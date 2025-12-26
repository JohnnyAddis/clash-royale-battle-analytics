import requests
from config import API_TOKEN
from urllib.parse import quote

def fetch_battle_log(player_tag):
    encoded_tag = quote(player_tag, safe="")
    url = f"https://api.clashroyale.com/v1/players/{encoded_tag}/battlelog"
    

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()