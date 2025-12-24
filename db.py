# db.py
import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def ingest_battle(conn, battle):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO players (player_tag, player_name)
            VALUES (%s, %s)
            ON CONFLICT (player_tag) DO NOTHING;
            """,
            (battle["player_tag"], battle["player_name"])
        )

        cur.execute(
            """
            INSERT INTO decks (deck_signature)
            VALUES (%s)
            ON CONFLICT (deck_signature) DO NOTHING;
            """,
            (battle["deck_signature"],)
        )

        cur.execute(
            """
            INSERT INTO battles (
                player_tag,
                battle_time,
                opponent_tag,
                deck_signature,
                win,
                game_mode
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (
                battle["player_tag"],
                battle["battle_time"],
                battle["opponent_tag"],
                battle["deck_signature"],
                battle["win"],
                battle["game_mode"],
            )
        )

    conn.commit()
