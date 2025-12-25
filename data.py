import time
from api import fetch_battle_log
from parser import parse_battle
from db import get_connection, ingest_battle, get_deck_win_rates, get_mode_win_rates, get_time_series_win_rates, get_active_players, update_last_polled_at, update_last_seen_at
from config import PLAYER_TAG

POLLING_INTERVAL_SECONDS = 5 #10 minutes for now


def poll_once(conn, player_tag):
    battles = fetch_battle_log(player_tag)

    inserted = 0

    for raw in battles:
        parsed = parse_battle(raw)
        if parsed is None:
            continue

        if ingest_battle(conn, parsed):
            inserted += 1

    update_last_polled_at(conn, player_tag)

    if inserted > 0:
        update_last_seen_at(conn, player_tag)

    print(f"[poll] processed {len(battles)} battles | new: {inserted}")



def main():
    conn = get_connection()
    print('Started polling. ctr c to stop.')

    try:
        while True:
            try:
                active_players = get_active_players(conn)
                print(f"[debug] active players from DB: {active_players}")
                for player_tag in active_players:
                    poll_once(conn, player_tag)
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
