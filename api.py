import requests
from config import API_TOKEN

def fetch_battle_log(player_tag):
    url = f"https://api.clashroyale.com/v1/players/%23{player_tag}/battlelog"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()