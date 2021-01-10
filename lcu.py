import requests
import lcu_connector_python as lcu
from requests.auth import HTTPBasicAuth
import json

connect = lcu.connect("/mnt/c/Riot Games/League of Legends/LeagueClient.exe")
print(connect)
url = connect['url']
port = connect['port']

url = f"{'https'}://{connect['url']}"
print(url)

def makeRequest(endpoint, body, method):
  if method == "POST":
    r = requests.post(
      url+ endpoint, 
      auth=('riot', connect['authorization']), 
      data=body, 
      headers={'Accept': 'application/json'}
    )
    return r.json()
  elif method == "GET":
    r = requests.get(url + endpoint, auth=('riot', connect['authorization']))
    return r.json()

GAME_ID = 3705698442
# metadata = makeRequest(f'/lol-replays/v2/metadata/{GAME_ID}/create', 
#   {
#     "gameEnd": 1626, 
#     "gameType": "MATCHED_GAME",
#     "gameVersion": "10.25.348.1797",
#     "queueId": 420
#   }, 'POST')

# metadata = makeRequest(f'/lol-replays/v1/metadata/{GAME_ID}/create/gameVersion/10.25.348.1797/gameType/queue/420', {}, 'POST')
metadata = makeRequest(f'/lol-replays/v1/metadata/{GAME_ID}', {}, 'GET')
print(metadata)
download = makeRequest(f'/lol-replays/v1/rofls/{GAME_ID}/download', {'componentType': 'string'}, 'POST')
print(download)
# metadata = makeRequest(f'/lol-replays/v1/rofls/path/default', {}, 'GET')

# metadata = makeRequest('/lol-replays/v1/configuration', {}, 'GET')
# print(metadata)
  