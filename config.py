import os

API_TOKEN = os.getenv("CLASH_API_TOKEN")
PLAYER_TAG = "L92QYYC0"

RANKED_MODE_ID = 72000450
TROPHY_MODE_ID = 72000006

DB_CONFIG = {
    "host": "localhost",
    "dbname": "clash_royale",
    "user": "postgres",
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": 5432
}

if API_TOKEN is None:
    raise RuntimeError("CLASH_API_TOKEN not set")

if DB_CONFIG["password"] is None:
    raise RuntimeError("POSTGRES_PASSWORD not set")


