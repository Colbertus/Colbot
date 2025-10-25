"""
Module Docstring Placeholder
"""
# Imports
import os

import aiohttp


# Class used for the OpenWeatherAPI service
class APIService:
    """
    Class docstring placeholder
    """

    def __init__(self):

        # When setting up an instance of the class, make sure that the endpoints are set
        self.base_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.api_key = os.getenv("OW_API_KEY")

    # Asyncronous function used to query weather information
    async def fetch_lat_long(self, query: str):
        """
        Method docstring placeholder
        """

        # Initialize the endpoint and the parameters for the OpenWeather query
        endpoint = self.base_url
        params = {"q": query, "limit": 1, "appid": self.api_key}

        # Start the ClientSession and perform the API call
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:

                # If the response status was good, then return the data
                if response.status == 200:

                    data = await response.json()

                    if data == []:
                        return None, None

                    lat = data[0]["lat"]
                    long = data[0]["lon"]

                    return lat, long

                # If the response happened to be one of an error

                if response.status == 404:
                    raise ValueError(f"No data found for query: {query}")
