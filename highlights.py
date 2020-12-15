from riotwatcher import LolWatcher, ApiError
from pprint import pprint
import datetime
import time
from secret import get_api_key

watcher = LolWatcher(get_api_key())
region = 'na1'

# USER
USERNAME = 'blaberfish2'
LANE = 'JUNGLE'
ROLE = 'NONE'
RANKED_ID = 420

# TIME, get month start/end in seconds
my_date = datetime.datetime(2020, 12, 1)
first_day_this_month = datetime.datetime(my_date.year, my_date.month, 1)
month_start = time.mktime(first_day_this_month.timetuple())
some_day_next_month = first_day_this_month + datetime.timedelta(days=32)
first_day_next_month = datetime.datetime(some_day_next_month.year, some_day_next_month.month, 1)
last_second_this_month = first_day_next_month - datetime.timedelta(seconds=1)
month_end = time.mktime(last_second_this_month.timetuple())

# USER
user = watcher.summoner.by_name(region, USERNAME)
matches = watcher.match.matchlist_by_account(region, user['accountId'])

res = []
for match in matches['matches']:
  # Only want ranked games
  if match['queue'] != RANKED_ID:
    continue

  # Only want on role games
  if match['lane'] != LANE or match['role'] != ROLE:
    continue

  # League timestamp is in ms
  # timestamp = match['timestamp'] / 1000
  # if timestamp < month_start or timestamp > month_end:
  #   print(timestamp)
  #   continue

  res.append(match)

for match in res:
  print(match)

  match_info = watcher.match.by_id(region, match['gameId'])

  # Get the participant ID fro match info
  participant_id = None
  for participant in match_info['participantIdentities']:
    if participant['player']['accountId'] == user['accountId']:
      participant_id = participant['participantId']
      # print(participant)

  # For match participant info
  # for participant in match_info['participants']:
  #   if participant['participantId'] == participant_id:
  #     print(participant['stats']['tripleKills'])
  #     print(participant['stats']['quadraKills'])
  #     print(participant['stats']['pentaKills'])

  timeline = watcher.match.timeline_by_match(region, match['gameId'])
  # 1 frame per min
  print(timeline.keys())
  print(len(timeline['frames']))
  print(timeline['frameInterval'])
  for frame in timeline['frames']:
    for event in frame['events']:
      if event['type'] == 'CHAMPION_KILL' and event['killerId'] == participant_id:
        print(event)
    
  break
