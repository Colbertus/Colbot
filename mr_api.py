import requests
import json

def gift_codes(): 
  try: 
    response = requests.get('https://mrapi.org/api/codes')
    response.raise_for_status()

    json_data = json.loads(response.text)

    giftCodes = "Reward: " + json_data[0]['rewards'] + "\nCode: " + json_data[0]['code'] + "\nExpiration: " + json_data[0]['expiringDate']

    return giftCodes

  except requests.exceptions.RequestException as e:
    error = f"An error occurred: {e}"
    return error
  
def player_id(name):
    try: 
       
       response = requests.get('https://mrapi.org/api/player-id/' + name)
       response.raise_for_status()

       json_data = json.loads(response.text)


       playerID = "Name: " + json_data['name'] + "\nID: " + json_data['id']
       
       return playerID
    except requests.exceptions.RequestException as e:
       error = f"An error occurred: {e}"
       return error 