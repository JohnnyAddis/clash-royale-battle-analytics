"""
First time using fastapi, not sure exactly what i am doing but my goal is to:
1) create fastapi app
2)define routes
3) call the basic analytics functions i just wrote from db.py
"""

# api_server.py
from fastapi import FastAPI
from db import (
    get_connection,
    get_deck_win_rates,
    get_mode_win_rates,
    get_time_series_win_rates,
)

app = FastAPI(
    title="Clash Royale Battle Analytics API",
    description="Analytics backend for Clash Royale battle data",
    version="0.1.0",
)


@app.get("/analytics/decks")
def deck_win_rates():
    conn = get_connection()
    try:
        return get_deck_win_rates(conn)
    finally:
        conn.close()


@app.get("/analytics/modes")
def mode_win_rates():
    conn = get_connection()
    try:
        return get_mode_win_rates(conn)
    finally:
        conn.close()


@app.get("/analytics/timeseries")
def time_series():
    conn = get_connection()
    try:
        return get_time_series_win_rates(conn)
    finally:
        conn.close()
