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

        inserted = cur.rowcount == 1

    conn.commit()
    return inserted

def register_player(conn, player_tag, player_name=None):
    query = """
        INSERT INTO players (player_tag, player_name, is_active)
        VALUES (%s, %s, TRUE)
        ON CONFLICT (player_tag)
        DO UPDATE SET
            is_active = TRUE,
            player_name = COALESCE(EXCLUDED.player_name, players.player_name);
    """
    with conn.cursor() as cur:
        cur.execute(query, (player_tag, player_name))
    conn.commit()

#used for GET /players endpoint to show system state. mainly for debugging purposes atm.
def get_players(conn):
    query = """
        SELECT
            player_tag,
            player_name,
            is_active,
            last_polled_at,
            last_seen_at,
            created_at
        FROM players
        ORDER BY created_at DESC;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

    return [
        {
            "player_tag": r[0],
            "player_name": r[1],
            "is_active": r[2],
            "last_polled_at": r[3],
            "last_seen_at": r[4],
            "created_at": r[5],
        }
        for r in rows
    ]

def get_player_by_tag(conn, player_tag):
    query = """
        SELECT
            player_tag,
            player_name,
            is_active,
            last_polled_at,
            last_seen_at,
            created_at
        FROM players
        WHERE player_tag = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (player_tag,))
        row = cur.fetchone()

    if row is None:
        return None

    return {
        "player_tag": row[0],
        "player_name": row[1],
        "is_active": row[2],
        "last_polled_at": row[3],
        "last_seen_at": row[4],
        "created_at": row[5],
    }



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

#db write
def update_last_polled_at(conn,player_tag):
    query = """
        UPDATE players
        SET last_polled_at = NOW()
        WHERE player_tag = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (player_tag,))
    conn.commit()

def update_last_seen_at(conn, player_tag):
    query = """
    UPDATE players
    SET last_seen_at = NOW()
    WHERE player_tag = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (player_tag,))
    conn.commit()

def mark_player_inactive(conn, player_tag: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE players
            SET is_active = FALSE
            WHERE player_tag = %s;
            """,
            (player_tag,)
        )
    conn.commit()

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
