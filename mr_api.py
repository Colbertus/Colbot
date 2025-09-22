import requests
import json
import os
import http.client
from dotenv import load_dotenv

load_dotenv("token.env")

MR_API_KEY = os.getenv("MR_API_KEY")

header = {
    'X-API-Key': MR_API_KEY
}
  
def player_id(name):
    try: 
       
       URL = "https://marvelrivalsapi.com/api/v1/find-player/" + name
       response = requests.get(URL, headers=header)
       response.raise_for_status()

       json_data = json.loads(response.text)

       playerID = (
        "**Name:** *" + json_data['name'] + "*" 
        "\n**ID:** *" + json_data['uid'] + "*"
       )
       
       return playerID
    except requests.exceptions.RequestException as e:
       error = f"An error occurred: {e}"
       return error 

def player_stats(ID):
  # TODO: COME BACK TO THIS ONCE https://marvelrivalsapi.com/api/v2/player/Colbertus STARTS WORKING
  try:

    response = requests.get('https://mrapi.org/api/player/' + ID)
    response.raise_for_status()

    json_data = json.loads(response.text)

    playerName = json_data['player_name']
    playerID = json_data['player_uid']
    playerAchievements = json_data['achievements_completed']
    playerLevel = json_data['stats']['level']
    playerRank = json_data['stats']['rank']['rank']
    ranked_kdr = json_data['stats']['ranked']['kdr']
    unranked_kdr = json_data['stats']['unranked']['kdr']

    stats = (
      "## Stats for Player: " + playerName + 
      " (ID: " + playerID + ") ##\n" 
      "- **Number of Achievements:** " + "*" + playerAchievements + "*" + "\n"
      "- **Player Level:** " + "*" + playerLevel + "*" + "\n"
      "- **Player Rank:** " + "*" + playerRank + "*" + "\n"
      "- **Unranked K/D:** " + "*" + unranked_kdr + "*" + "\n"
      "- **Ranked K/D:** " + "*" + ranked_kdr + "*" +"\n"
    )

    return stats

  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error

def character_stats(character):

  character = character.replace(" ", "_")
  character = character.replace("&_", "")
  character = character.replace("_The_Land_Shark", "")

  try: 
    response = requests.get('https://mrapi.org/api/hero/' + character)
    response.raise_for_status()

    json_data = json.loads(response.text)

    headshot_image_URL = str(json_data['image_square'])
    character_name = json_data['name']

    pc_quickplay_appearance_rate = str(json_data['meta'][0]['appearance_rate']) + "%"
    pc_quickplay_win_rate = str(json_data['meta'][0]['win_rate']) + "%"

    pc_ranked_appearance_rate = str(json_data['meta'][1]['appearance_rate']) + "%"
    pc_ranked_win_rate = str(json_data['meta'][1]['win_rate']) + "%"

    console_quickplay_appearance_rate = str(json_data['meta'][8]['appearance_rate']) + "%"
    console_quickplay_win_rate = str(json_data['meta'][8]['win_rate']) + "%"

    console_ranked_appearance_rate = str(json_data['meta'][9]['appearance_rate']) + "%"
    console_ranked_win_rate = str(json_data['meta'][9]['win_rate']) + "%"

    stats = (
      headshot_image_URL + "\n"
      "## Stats for Character: " + character_name + " ##\n"
      "- **PC Quickplay Appearance Rate:** " + "*" + pc_quickplay_appearance_rate + "*" + "\n"
      "- **PC Quickplay Win Rate:** " + "*" + pc_quickplay_win_rate + "*" + "\n\n"
      "- **PC Ranked Appearance Rate:** " + "*" + pc_ranked_appearance_rate + "*" + "\n"
      "- **PC Ranked Win Rate:** " + "*" + pc_ranked_win_rate + "*" + "\n\n"
      "- **Console Quickplay Appearance Rate:** " + "*" + console_quickplay_appearance_rate + "*" + "\n"
      "- **Console Quickplay Win Rate:** " + "*" + console_quickplay_win_rate + "*" + "\n\n"
      "- **Console Ranked Appearance Rate:** " + "*" + console_ranked_appearance_rate + "*" + "\n"
      "- **Console Ranked Win Rate:** " + "*" + console_ranked_win_rate + "*"
    )

    return stats
  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error

def character_names():

  try: 
    response = requests.get('https://marvelrivalsapi.com/api/v1/heroes', headers=header)
    response.raise_for_status()

    json_data = json.loads(response.text)
    vanguardList = []
    duelistList = []
    strategistList = []

    for index in range(len(json_data)):
      name = json_data[index]['name']
      role = json_data[index]['role']
      realName = json_data[index]['real_name']
      if role == "Vanguard":
        vanguardList.append(name, realName)
      elif role == "Duelist":
        duelistList.append(name, realName)
      elif role == "Strategist":
        strategistList.append(name, realName)
      else:
        print("ERROR HAS OCCURRED, ROLE: " + role + " IS NOT VALID!")
      
    

    return vanguardList, duelistList, strategistList

  except requests.exceptions.RequestException as e:
    error: f"An error occurred: {e}"
    return error 

def rank_totals():

  try: 
    response = requests.get('https://mrapi.org/api/ranks')
    response.raise_for_status()

    json_data = json.loads(response.text)

    totals = []

    for rank, values in json_data.items():
      if '1' in values and '2' in values and '3' in values:
        totals.append(values['1'])
        totals.append(values['2'])
        totals.append(values['3'])
      elif 'total' in values:
        totals.append(values['total'])
    
    count = 0
    rank = 1

    rank_total = (
      "## Rank Totals: ##\n"
      "\n- ***Bronze:***\n"
    )

    for index, value in enumerate(totals):

      if index == 21:
        rank_total += "\n- ***Eternity:***\n"
        rank_total += "**Total:** *" + str(value) + "*\n"
      elif index == 22:
        rank_total += "\n- ***One Above All:***\n"
        rank_total += "**Total:** *" + str(value) + "*\n"

      else:
        count += 1
        rank_total += "**" + str(count) + ":** *" + str(value) + "*\n"

        if count % 3 == 0:
          if rank == 1:
            rank_total += "\n- ***Silver:***\n"
            rank += 1
            count = 0
          elif rank == 2:
            rank_total += "\n- ***Gold:***\n"
            rank += 1
            count = 0
          elif rank == 3:
            rank_total += "\n- ***Platinum:***\n"
            rank += 1
            count = 0
          elif rank == 4:
            rank_total += "\n- ***Diamond:***\n"
            rank += 1
            count = 0
          elif rank == 5:
            rank_total += "\n- ***Grandmaster:***\n"
            rank += 1
            count = 0
          elif rank == 6:
            rank_total += "\n- ***Celestial:***\n"
            rank += 1
            count = 0
    
    return rank_total
      

  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error
