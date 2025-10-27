"""
Module Docstring Placeholder
"""

# Imports
import os
from typing import Sequence, TypeAlias, Union

import aiohttp

# Define the acceptable scalar types for Aiohttp parameters
AiohttpParamValue: TypeAlias = Union[str, int, float]

# Define the full type for the 'params' dictionary
AiohttpParams: TypeAlias = dict[
    str, Union[AiohttpParamValue, Sequence[AiohttpParamValue]]
]


# Class used for the OpenWeatherAPI service
class APIService:
    """
    Class docstring placeholder
    """

    def __init__(self) -> None:

        # When setting up an instance of the class, make sure that the endpoints are set
        self.base_url: str = "https://api.openweathermap.org/geo/1.0/direct"
        self.api_key: str = os.getenv("OW_API_KEY", "EMPTY")

    # Asyncronous function used to query weather information
    async def fetch_lat_long(self, query: str) -> tuple[float, float]:
        """
        Method docstring placeholder
        """

        # Initialize the endpoint and the parameters for the OpenWeather query
        endpoint = self.base_url
        params: AiohttpParams = {"q": query, "limit": 1, "appid": self.api_key}

        # Start the ClientSession and perform the API call
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:

                # If the response status was good, then return the data
                if response.status == 200:

                    data = await response.json()

                    if data == []:
                        return 0.0, 0.0

                    lat = data[0]["lat"]
                    long = data[0]["lon"]

                    return lat, long

                # If the response happened to be one of an error

                if response.status == 404:
                    raise ValueError(f"No data found for query: {query}")

            return 0.0, 0.0
