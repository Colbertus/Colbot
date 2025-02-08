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
      "## Stats for player: " + playerName + 
      " (ID: " + playerID + ") ##\n" 
      "- **Number of Achievements:** " + "*" + playerAchievements + "*" + "\n"
      "- **Player Level:** " + "*" + playerLevel + "*" + "\n"
      "- **Player Rank:** " + "*" + playerRank + "*" +"\n"
      "- **Unranked K/D:** " + "*" + unranked_kdr + "*" + "\n"
      "- **Ranked K/D:** " + "*" + ranked_kdr + "*" +"\n"
    )

    return stats

  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error

