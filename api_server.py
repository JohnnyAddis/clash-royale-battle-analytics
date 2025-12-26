from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import (
    get_connection,
    register_player,
    get_deck_win_rates,
    get_mode_win_rates,
    get_time_series_win_rates,
    get_players,
    get_player_by_tag
)
from fastapi.middleware.cors import CORSMiddleware
from parser import normalize_player_tag


app = FastAPI(
    title="Clash Royale Battle Analytics API",
    description="Analytics backend for Clash Royale battle data",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class PlayerRegisterRequest(BaseModel):
    player_tag: str
    player_name: str | None = None

# @app.post("/players/register")
# def register_player_endpoint(req: PlayerRegisterRequest):
#     if not req.player_tag.startswith("#"):
#         raise HTTPException(status_code=400, detail="Invalid player tag format")

#     try:
#         profile = fetch_player_profile(req.player_tag)
#     except Exception:
#         raise HTTPException(status_code=400, detail="Player tag does not exist")

#     conn = get_connection()
#     try:
#         register_player(
#             conn,
#             player_tag=req.player_tag,
#             player_name=profile["name"]  # authoritative name
#         )
#     finally:
#         conn.close()


@app.post("/players/register")
def register_player_endpoint(req: PlayerRegisterRequest):
    print("REGISTER TAG RECEIVED:", repr(req.player_tag))

    if not req.player_tag.startswith("#"):
        raise HTTPException(status_code=400, detail="Invalid player tag")

    conn = get_connection()
    try:
        register_player(
            conn,
            player_tag=req.player_tag,
            player_name=req.player_name
        )
    finally:
        conn.close()

    return {
        "status": "ok",
        "player_tag": req.player_tag
    }

    # good
    return {
        "status": "ok",
        "player_tag": req.player_tag,
        "player_name": profile["name"],
    }


@app.get("/players/{player_tag}")
def get_player(player_tag: str):
    conn = get_connection()
    try:
        player = get_player_by_tag(conn, player_tag)
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    finally:
        conn.close()

@app.get("/players")
def list_players():
    conn = get_connection()
    try:
        return get_players(conn)
    finally:
        conn.close()



@app.get("/analytics/decks/{player_tag}")
def deck_win_rates(player_tag: str):
    player_tag = normalize_player_tag(player_tag)

    conn = get_connection()
    try:
        return get_deck_win_rates(conn, player_tag)
    finally:
        conn.close()



@app.get("/analytics/modes")
def mode_win_rates(player_tag: str):
    conn = get_connection()
    try:
        return get_mode_win_rates(conn, player_tag)
    finally:
        conn.close()


@app.get("/analytics/timeseries")
def time_series(player_tag: str):
    conn = get_connection()
    try:
        return get_time_series_win_rates(conn, player_tag)
    finally:
        conn.close()