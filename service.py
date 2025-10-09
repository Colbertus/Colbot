# Imports 
import os
import aiohttp
import json

# Class used for the OpenWeatherAPI service 
class APIService:

    def __init__(self):

        # When setting up an instance of the class, make sure that the endpoints are set 
        self.BASE_URL = "https://api.openweathermap.org/geo/1.0/direct"
        self.API_KEY = os.getenv("OW_API_KEY")

    # Asyncronous function used to query weather information
    async def fetch_lat_long(self, query: str):

        # Initialize the endpoint and the parameters for the OpenWeather query 
        endpoint = self.BASE_URL
        params = {
            "q": query,
            "limit": 1,
            "appid": self.API_KEY
            }

        # Start the ClientSession and perform the API call
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:

                # If the response status was good, then return the data 
                if response.status == 200:

                    data = await response.json()
                    lat = data[0]['lat']
                    long = data[0]['lon']

                    return lat, long
                
                # If the response happened to be one of an error 
                elif response.status == 404:
                    raise ValueError(f"No data found for query: {query}")
                else:
                    raise Exception(f"API Error: Status {response.status}")