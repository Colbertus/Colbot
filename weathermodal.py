import discord
import string
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
            required = False
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
       
        city_input = self.children[0].value
        state_input = self.children[1].value
        country_input = self.children[2].value
        intPresent = False
        symbolPresent = False

        input_list = [city_input, state_input, country_input]

        for input in input_list:

            anySymbols = any(char in string.punctuation for char in input)
            if anySymbols == True:
                symbolPresent = True

            try:
                int(input)
                intPresent = True
            except ValueError:
                continue
        
        if intPresent or symbolPresent:
            embed = discord.Embed(
               title = f"Please enter in valid input to find latitude and longitude",
               color = discord.Color.dark_purple()
            )
            await interaction.response.send_message(embed = embed)
        else:

            query_parts = [p.strip() for p in [city_input, state_input, country_input]]
            api_query = ",".join(query_parts)
            await self.cog.output_lat_long(query = api_query, ctx = interaction)
