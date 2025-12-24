# data.py
from api import fetch_battle_log
from parser import parse_battle
from db import get_connection, ingest_battle
from config import PLAYER_TAG

def main():
    battles = fetch_battle_log(PLAYER_TAG)
    conn = get_connection()

    inserted = 0
    for raw in battles:
        parsed = parse_battle(raw)
        if parsed is None:
            continue

        ingest_battle(conn, parsed)
        inserted += 1

    conn.close()
    print(f"Processed {inserted} battles")

if __name__ == "__main__":
    main()
