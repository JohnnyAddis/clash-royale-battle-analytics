# import requests
# import json
# from datetime import datetime, timezone
# import psycopg2
# API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJiNTljMzI2LTM2NWQtNDcyMS1hOGM0LTA1NzQxNzRiNWNmMiIsImlhdCI6MTc2NjYwNjk1NCwic3ViIjoiZGV2ZWxvcGVyLzE4ZDNmOGQzLTMxYzUtOThjMi1kNmU4LThkY2NjMGRiN2E3NyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3Ni4xMzYuODUuMTc0Il0sInR5cGUiOiJjbGllbnQifV19.o7lMESPe3daou98e00X4RumPWqzaGmO13u5wGk6VJxjs6ogBRW5IZmPiVJz-yoQtQxNoEAE_2Uc-3RuHx0HDfg'
# my_tag = 'L92QYYC0'
# RANKED_MODE_ID = 72000450
# TROPHY_MODE_ID = 72000006


# url = f'https://api.clashroyale.com/v1/players/%23{my_tag}/battlelog'


# headers = {
#     "Accept": "application/json",
#     "Authorization": f"Bearer {API_TOKEN}"
# }


# #returns string unqiue to each deck, regardless of order, accounts for evos/heros
# def sign_deck(deck):
#     #Same deck, same signature every time (including evos/heros)
#     deckTokens = []
#     for card in deck:
        
#         if 'evolutionLevel' in card:
#             if card['evolutionLevel'] == 1:
#                 deckTokens.append(f'{card['id']}_EVO')
#             elif card['evolutionLevel'] == 2:
#                 deckTokens.append(f'{card['id']}_HERO')
#         else: 
#             deckTokens.append(f'{card['id']}_NORMAL')
#     #sorting gets rid of issue with same decks different order
#     deckTokens.sort()
#     deckSignature = "|".join(deckTokens) #joining with delimiter that does not appear in card IDs
#     return deckSignature

# #win or loss, and for what game mode
# def getResult(game_mode, battle):
#     if game_mode == 'TROPHY':
#         if battle['team'][0]['trophyChange'] > 0:
#             return True
#         else:
#             return False
#     elif game_mode == 'RANKED':
#         my_crowns = battle['team'][0]['crowns']
#         opp_crowns = battle['opponent'][0]['crowns']
#         if my_crowns > opp_crowns:
#             return True
#         else:
#             return False

# #returns game mode, i am only caring about ranked/trophy modes, so other modes i will be throwing out
# def getMode(id):
#     if id == RANKED_MODE_ID:
#         return 'RANKED'
#     elif id == TROPHY_MODE_ID:
#         return 'TROPHY'
#     else:
#         return 'invalid mode'

# #returns datetime object in good form to send to postgres
# def getBattleTime(battle):
#     rawTime = battle['battleTime']

#     battleTime = datetime.strptime(
#     rawTime,
#     "%Y%m%dT%H%M%S.%fZ"
#     ).replace(tzinfo=timezone.utc)
#     return battleTime

# #returns parsed fields from returned json necessary to give to postgres
# def parse_battle(battle):
#     mode = getMode(battle['gameMode']['id'])
#     if mode == 'invalid mode':
#         return None
#     return {
#         'game_mode' : mode,
#         'player_tag' : my_tag,
#         'player_name' : battle['team'][0]['name'],
#         'opponent_tag' : battle['opponent'][0]['tag'],
#         'deck_signature' : sign_deck(battle['team'][0]['cards']),
#         'battle_time' : getBattleTime(battle),
#         'win' : getResult(getMode(battle['gameMode']['id']), battle)
#     }


# response = requests.get(url, headers=headers)
# print(response.status_code)
# if response.status_code == 200:
#     player_data = response.json()
    

# # print(player_data[0]['team'][0]['cards'])
# print(parse_battle(player_data[1]))



# # #alright lets do some sql lol

# # #establish connection
# # conn = psycopg2.connect(host='localhost',dbname = 'clash_royale', user = 'postgres', password = 'Bear2642', post = 5432)

# # #cursor to execute commands
# # cur = conn.cursor()

# # #db stuff:
# # cur.execute("""CREATE TABLE IF NOT EXISTS 
# # """)




# # #commit to db, close cursor and connection

# # conn.commit()
# # cur.close()
# # conn.closer