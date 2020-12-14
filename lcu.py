import requests
import lcu_connector_python as lcu
from requests.auth import HTTPBasicAuth

connect = lcu.connect("/mnt/c/Riot Games/League of Legends/LeagueClient.exe")
print(connect)
url = connect['url']
port = connect['port']

url = f"{connect['connection_method']}://{connect['url']}"
print(url)

r = requests.get(url + '/lol-summoner/v1/current-summoner', auth=('riot', connect['authorization']))
print(r.content)
