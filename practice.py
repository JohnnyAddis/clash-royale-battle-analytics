from db import get_active_players, get_connection


conn = get_connection()
print(get_active_players(conn))