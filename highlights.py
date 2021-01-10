from riotwatcher import LolWatcher, ApiError
from pprint import pprint
import datetime
import time
from secret import get_api_key
from champions import get_champions_name

watcher = LolWatcher(get_api_key())
region = 'na1'

# USER
# USERNAME = 'blaberfish2'
# LANE = 'JUNGLE'
# ROLE = 'NONE'
# USERNAME = 'C9 Zven'
# LANE = 'BOTTOM'
# ROLE = 'DUO_CARRY'
USERNAME = 'humanbenchmark'
LANE = 'MID'
ROLE = 'SOLO'
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

print('For ranked on role games, found', len(res), 'games')

for match in res[:20]:
  match_info = watcher.match.by_id(region, match['gameId'])
  game_end = match_info["gameDuration"]
  game_type = match_info["gameType"]
  game_version = match_info["gameVersion"]
  queue_id = match_info["queueId"]

  # Get the participant ID fro match info
  participant_id = None
  for participant in match_info['participantIdentities']:
    if (participant['player']['accountId'] == user['accountId'] or 
        participant['player']['summonerName'] == USERNAME):
      participant_id = participant['participantId']
  is_multikill = False
  highlight_times = []
  kda = None

  # For match participant info
  for participant in match_info['participants']:
    if participant['participantId'] == participant_id:
      stats =  participant['stats']
      triple = stats['tripleKills']
      quadra = stats['quadraKills']
      penta = stats['pentaKills']
      kda = f"{stats['kills']}/{stats['deaths']}/{stats['assists']}"
      if triple > 0 or quadra > 0 or penta > 0:
        is_multikill = True
  
  is_highlight = is_multikill
  timeline = watcher.match.timeline_by_match(region, match['gameId'])
  # 1 frame per min
  all_kill_times = []
  for frame in timeline['frames']:
    for event in frame['events']:
      if event['type'] == 'CHAMPION_KILL' and event['killerId'] == participant_id:

        if len(event['assistingParticipantIds']) == 0:
          highlight_times.append({'time': event['timestamp'] / (1000 * 60), 'info': 'solo_kill'})
          is_highlight = True

        all_kill_times.append(event['timestamp'])

  if is_multikill:
    kt_diff = []
    for i in range(len(all_kill_times)):
      if i == 0:
        kt_diff.append(0)
      else:
        kt_diff.append((all_kill_times[i] - all_kill_times[i-1]) / 1000)

    for i in range(len(kt_diff)):
      if i == 0:
        continue
      if kt_diff[i] < 10:
        highlight_times.append({'time': all_kill_times[i-1] /(1000 * 60), 'info': 'multikill'})

  if is_highlight and len(highlight_times) > 0:
    print("game_id", match['gameId'])
    print("champion", get_champions_name(match['champion']))
    print("kda", kda)
    print(highlight_times)
  print("champion", get_champions_name(match['champion']))
  print("kda", kda)

  time.sleep(1)
