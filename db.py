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

#this should just be a db read, return players with active status assigned to them
def get_active_players(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT player_tag
            FROM players
            WHERE is_active = TRUE;
            """
        )
        rows = cur.fetchall()
    return [row[0] for row in rows]


def get_deck_win_rates(conn):
    """
    Returns win rate statistics per deck (RANKED/TROPHY MODE ONLY).
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                deck_signature,
                COUNT(*) AS games,
                SUM(win::int) AS wins,
                ROUND(AVG(win::int) * 100, 2) AS win_rate
            FROM battles
            GROUP BY deck_signature
            ORDER BY win_rate DESC;
            """
        )

        rows = cur.fetchall()

    results = []
    for deck_signature, games, wins, win_rate in rows:
        results.append({
            "deck_signature": deck_signature,
            "games": games,
            "wins": wins,
            "win_rate": win_rate
        })

    return results


def get_mode_win_rates(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                game_mode,
                COUNT(*) AS games,
                SUM(win::int) AS wins,
                ROUND(AVG(win::int) * 100, 2) AS win_rate
            FROM battles
            GROUP BY game_mode;
            """
        )

        rows = cur.fetchall()

    return [
        {
            "game_mode": game_mode,
            "games": games,
            "wins": wins,
            "win_rate": win_rate,
        }
        for game_mode, games, wins, win_rate in rows
    ]


def get_time_series_win_rates(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                DATE(battle_time) AS day,
                COUNT(*) AS games,
                ROUND(AVG(win::int) * 100, 2) AS win_rate
            FROM battles
            GROUP BY day
            ORDER BY day;
            """
        )
        rows = cur.fetchall()
        return [
        {
            "date": day,
            "games": games,
            "win_rate": win_rate,
        }
        for day, games, win_rate in rows
    ]
