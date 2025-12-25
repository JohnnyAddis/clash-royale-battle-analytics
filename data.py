import time
from api import fetch_battle_log
from parser import parse_battle
from db import get_connection, ingest_battle
from config import PLAYER_TAG

POLLING_INTERVAL_SECONDS = 600 #10 minutes for now


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
    try:
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
