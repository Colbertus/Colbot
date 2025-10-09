import discord
from discord.ui import Modal, TextInput

class WeatherModal(Modal, title = 'Weather Lookup'):


    def __init__(self, cog_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cog = cog_instance
        self.timeout = 120.0

        city = TextInput(
            label = "City Name",
            placeholder = "e.g. London",
            max_length = 50,
            required = True
        )

        state = TextInput(
            label = "State/Region",
            placeholder = "e.g. AL, TN",
            max_length = 50,
            required = True
        )

        country = TextInput(
            label = "Country Code",
            placeholder = "e.g. US, FR, GB",
            max_length = 5,
            required = True
        )

        self.add_item(city)
        self.add_item(state)
        self.add_item(country)

    async def on_submit(self, interaction: discord.Interaction):
       
       city_input = str(self.children[0].value)
       state_input = str(self.children[1].value)
       country_input = str(self.children[2].value) 

       query_parts = [p.strip() for p in [city_input, state_input, country_input]]
       api_query = ",".join(query_parts)

       await self.cog.output_lat_long(query = api_query, ctx = interaction)
