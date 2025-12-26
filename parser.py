# parser.py
from datetime import datetime, timezone
from config import RANKED_MODE_ID, TROPHY_MODE_ID, PLAYER_TAG

def normalize_player_tag(tag: str) -> str:
    if not tag.startswith("#"):
        return f"#{tag}"
    return tag


def sign_deck(deck):
    deck_tokens = []

    for card in deck:
        if "evolutionLevel" in card:
            if card["evolutionLevel"] == 1:
                variant = "EVO"
            elif card["evolutionLevel"] == 2:
                variant = "HERO"
            else:
                variant = "NORMAL"
        else:
            variant = "NORMAL"

        deck_tokens.append(f"{card['id']}_{variant}")

    deck_tokens.sort()
    return "|".join(deck_tokens)


def get_mode(mode_id):
    if mode_id == RANKED_MODE_ID:
        return "RANKED"
    elif mode_id == TROPHY_MODE_ID:
        return "TROPHY"
    return None


def get_battle_time(battle):
    raw_time = battle["battleTime"]
    return datetime.strptime(
        raw_time,
        "%Y%m%dT%H%M%S.%fZ"
    ).replace(tzinfo=timezone.utc)


def get_result(game_mode, battle):
    team = battle["team"][0]
    opponent = battle["opponent"][0]

    # Primary, always-safe signal
    if "crowns" in team and "crowns" in opponent:
        return team["crowns"] > opponent["crowns"]

    # Fallback: use trophyChange if present
    if "trophyChange" in team:
        return team["trophyChange"] > 0

    # If we cannot determine result safely, skip this battle
    raise ValueError("Cannot determine battle result")


def parse_battle(battle):
    mode = get_mode(battle["gameMode"]["id"])
    if mode is None:
        return None

    try:
        win = get_result(mode, battle)
    except ValueError:
        return None  # skip this battle safely

    return {
        "game_mode": mode,
        "player_tag": PLAYER_TAG,
        "player_name": battle["team"][0]["name"],
        "opponent_tag": battle["opponent"][0]["tag"],
        "deck_signature": sign_deck(battle["team"][0]["cards"]),
        "battle_time": get_battle_time(battle),
        "win": win,
    }
