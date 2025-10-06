import os
import aiohttp

class APIService:

    def __init__(self):
        self.BASE_URL = "https://api.openweathermap.org/geo/1.0/direct"
        self.API_KEY = os.getenv("OW_API_KEY")

    async def fetch_data(self, query: str):
        endpoint = self.BASE_URL
        params = {
            "q": "Harvest,AL,USA",
            "limit": 1,
            "appid": self.API_KEY
            }

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:
                if response.status == 200:

                    data = await response.json()
                    return data
                elif response.status == 404:
                    raise ValueError(f"No data found for query: {query}")
                else:
                    raise Exception(f"API Error: Status {response.status}")