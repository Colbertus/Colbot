import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("token.env")
ow_api_key = os.getenv("OW_API_KEY")

def return_coord(city, state): 
    response = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + city + ',' + state + ',USA&limit=1&appid=' + ow_api_key)
    response.raise_for_status()

    json_data = json.loads(response.text)
    lat = json_data[0]['lat']
    long = json_data[0]['lon']

    return lat, long

def weather_info(lat, lon):
    response = requests.get('https://api.openweathermap.org/data/3.0/onecall?lat=' + lat + '&lon=' + lon + '&appid=' + ow_api_key)
    response.raise_for_status()

    json_data = json.loads(response.text)
    