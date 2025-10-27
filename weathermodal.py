"""
Module docstring placeholder
"""

# Imports
import string

import discord
from discord.ui import Modal, TextInput

from cog import APICog


# WeatherModal class that gets used for finding lat and long
class WeatherModal(Modal, title="Coordinate Lookup"):
    """
    Class docstring placeholder
    """

    # Initialize the class to contain the cog needed and the timeout for the modal object
    def __init__(self, cog_instance: APICog) -> None:
        super().__init__()
        self.cog = cog_instance
        self.timeout = 120.0

        # City input for the modal object that contain the placeholder, maximum length,
        # and whether it is actually required or not
        self.add_item(
            TextInput(
                label="City Name",
                placeholder="e.g. London",
                max_length=50,
                required=True,
            )
        )

        # State input for the modal object that contain the placeholder, maximum length,
        # and whether it is actually required or not
        self.add_item(
            TextInput(
                label="State/Region",
                placeholder="e.g. AL, TN",
                max_length=50,
                required=False,
            )
        )

        # Country input for the modal object that contain the placeholder, maximum length,
        # and whether it is actually required or not
        self.add_item(
            TextInput(
                label="Country Code",
                placeholder="e.g. US, FR, GB",
                max_length=5,
                required=True,
            )
        )

    # For when the user submits the modal object
    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Function docstring placeholder
        """

        city_component = self.children[0]
        state_component = self.children[1]
        country_component = self.children[2]

        assert isinstance(city_component, TextInput)
        assert isinstance(state_component, TextInput)
        assert isinstance(country_component, TextInput)

        # Save the inputs to be the following
        city_input = city_component.value
        state_input = state_component.value
        country_input = country_component.value

        # Set the following flags for error handling later
        int_present = False
        symbol_present = False

        input_list = [city_input, state_input, country_input]

        # For each input that was entered from the modal object..
        for region in input_list:

            # Check the input for any symbols (@#$%^)
            any_symbols = any(char in string.punctuation for char in region)

            # If symbols are present in any of the inputs, then set the following flag to 'True'
            if any_symbols is True:
                symbol_present = True

            # Next check to see if the input is an integer using try/except block
            # If there are no integers present, continue on with processing
            try:
                int(region)
                int_present = True
            except ValueError:
                continue

        # If either the symbols or an integer is present, then create the proper embed object
        # with the error and send
        if int_present or symbol_present:
            embed = discord.Embed(
                title="Please enter in valid input to find latitude and longitude",
                color=discord.Color.dark_purple(),
            )
            await interaction.response.send_message(embed=embed)

        # Otherwise, piece together the API query and pass execution to the cog function to
        # finish the API command
        else:

            # Strip the whitespace from each input before combining it all together with commas
            query_parts = [p.strip() for p in [city_input, state_input, country_input]]
            api_query = ",".join(query_parts)
            await self.cog.output_lat_long(query=api_query, interaction=interaction)
