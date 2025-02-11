import requests
import json

def gift_codes(): 
  try: 
    response = requests.get('https://mrapi.org/api/codes')
    response.raise_for_status()

    json_data = json.loads(response.text)

    giftCodes = (
      "Reward: " + json_data[0]['rewards'] +
      "\nCode: " + json_data[0]['code'] +
      "\nExpiration: " + json_data[0]['expiringDate']
    )

    return giftCodes

  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error
  
def player_id(name):
    try: 
       
       response = requests.get('https://mrapi.org/api/player-id/' + name)
       response.raise_for_status()

       json_data = json.loads(response.text)


       playerID = (
        "Name: " + json_data['name'] + 
        "\nID: " + json_data['id']
       )
       
       return playerID
    except requests.exceptions.RequestException as e:
       error = f"An error occurred: {e}"
       return error 

def player_stats(ID):

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

    return stats, headshot_image_URL
  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error, error

def character_names():

  try: 
    response = requests.get('https://mrapi.org/api/heroes')
    response.raise_for_status()

    json_data = json.loads(response.text)
    names = []

    for index in range(len(json_data)):
      name = json_data[index]['name']
      names.append(name)

    character_list = (
      "Character Names to pick from: \n"
      "NOTE: please use one of the following heroes for the command argument\n"
    )

    count = 1

    for index in names:
      character_list += "Hero " + str(count) + ": " + str(index) + "\n"
      count += 1 

    return character_list

  except requests.exceptions.RequestException as e:
    error: f"An error occurred: {e}"
    return error 

