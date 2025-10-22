# Imports 
import string

import discord
from discord.ui import Modal, TextInput


# WeatherModal class that gets used for finding lat and long
class WeatherModal(Modal, title = 'Coordinate Lookup'):

    # Initialize the class to contain the cog needed and the timeout for the modal object
    def __init__(self, cog_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cog = cog_instance
        self.timeout = 120.0

        # City input for the modal object that contain the placeholder, maximum length, and whether it is actually required or not
        city = TextInput(
            label = "City Name",
            placeholder = "e.g. London",
            max_length = 50,
            required = True
        )

        # State input for the modal object that contain the placeholder, maximum length, and whether it is actually required or not
        state = TextInput(
            label = "State/Region",
            placeholder = "e.g. AL, TN",
            max_length = 50,
            required = False
        )

        # Country input for the modal object that contain the placeholder, maximum length, and whether it is actually required or not 
        country = TextInput(
            label = "Country Code",
            placeholder = "e.g. US, FR, GB",
            max_length = 5,
            required = True
        )

        # Make sure to add these objects to the modal UI for use
        self.add_item(city)
        self.add_item(state)
        self.add_item(country)

    # For when the user submits the modal object
    async def on_submit(self, interaction: discord.Interaction):
        
        # Save the inputs to be the following
        city_input = self.children[0].value
        state_input = self.children[1].value
        country_input = self.children[2].value

        # Set the following flags for error handling later
        intPresent = False
        symbolPresent = False

        input_list = [city_input, state_input, country_input]

        # For each input that was entered from the modal object..
        for input in input_list:
            
            # Check the input for any symbols (@#$%^)
            anySymbols = any(char in string.punctuation for char in input)

            # If symbols are present in any of the inputs, then set the following flag to 'True'
            if anySymbols == True:
                symbolPresent = True

            # Next check to see if the input is an integer using try/except block
            # If there are no integers present, continue on with processing
            try:
                int(input)
                intPresent = True
            except ValueError:
                continue
        
        # If either the symbols or an integer is present, then create the proper embed object object with the error and send
        if intPresent or symbolPresent:
            embed = discord.Embed(
               title = f"Please enter in valid input to find latitude and longitude",
               color = discord.Color.dark_purple()
            )
            await interaction.response.send_message(embed = embed)
        
        # Otherwise, piece together the API query and pass execution to the cog function to finish the API command
        else:
            
            # Strip the whitespace from each input before combining it all together with commas
            query_parts = [p.strip() for p in [city_input, state_input, country_input]]
            api_query = ",".join(query_parts)
            await self.cog.outputLatLong(query = api_query, ctx = interaction)
