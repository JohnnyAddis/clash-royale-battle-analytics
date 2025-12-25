import time
from api import fetch_battle_log
from parser import parse_battle
from db import get_connection, ingest_battle, get_deck_win_rates, get_mode_win_rates, get_time_series_win_rates, get_active_players
from config import PLAYER_TAG

POLLING_INTERVAL_SECONDS = 5 #10 minutes for now


def poll_once(conn):
    battles = fetch_battle_log(PLAYER_TAG)

    inserted = 0
    for raw in battles:
        parsed = parse_battle(raw)
        if parsed is None:
            continue

        ingest_battle(conn, parsed)
        inserted += 1

    print(f"[poll] processed {len(battles)} battles")


def main():
    conn = get_connection()
    print('Started polling. ctr c to stop.')

     # ---- TEMP: analytics test ----
     #win-rate by deck
    print("\nDeck win rates:")
    stats = get_deck_win_rates(conn)
    for s in stats:
        print(
            f"Deck: {s['deck_signature'][:30]}... | "
            f"Games: {s['games']} | "
            f"Win %: {s['win_rate']}"
        )
    print("-----------------------------\n")


    #win-rate by game mode
    print("\n Game Mode Win Rates:")
    stats = get_mode_win_rates(conn)
    for s in stats:
        print(
            f'Game Mode: {s['game_mode']} |'
            f'Games: {s['games']} |'
            f'Win %: {s['win_rate']}'
        )
    print("-----------------------------\n")



    print('\n Win-Rate by date:')
    stats = get_time_series_win_rates(conn)
    for s in stats:
        print(
            f'Date: : {s['date']} | '
            f'Games: {s['games']} |'
            f'Win %: {s['win_rate']} |'

        )
    print("-----------------------------\n")


    
    # ---- END TEMP ----
    try:
        active_players = get_active_players(conn)
        print(f"[debug] active players from DB: {active_players}")
        while True:
            try:
                poll_once(conn)
            except Exception as e:
                print(f'[error] polling failed: {e}')
            print(f'[sleep] waiting {POLLING_INTERVAL_SECONDS} seconds\n')
            time.sleep(POLLING_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print('\nPolling stopped by the user.')

    finally:
        conn.close()
        print('DB connection closed.')
if __name__ == "__main__":
    main()
