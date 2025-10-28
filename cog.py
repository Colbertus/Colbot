"""
Module Docstring Placeholder
"""

# Imports
import os

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from colbot import Colbot
from service import APIService
from weathermodal import WeatherModal

# This will be temporary but serves to create the needed guild object used to sync commands faster
load_dotenv("token.env")
ID = int(os.getenv("TEST_SERVER_ID", "0"))
test_guild = discord.Object(id=ID)


# Class used to store the commands for the OpenWeatherAPI
class APICog(commands.Cog):
    """
    Class docstring placeholder
    """

    def __init__(self, bot: Colbot) -> None:

        # Initialize both the bot and the API Service
        self.bot = bot
        self.api_service = APIService()

    # Discord Command: city_lookup
    @app_commands.guilds(test_guild)
    @app_commands.command(name="city_lookup")
    async def city_lookup(self, interaction: discord.Interaction) -> None:
        """
        Function docstring placeholder
        """

        # Setup the modal weather object that'll be used for the query before sending it
        modal = WeatherModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        query = modal.api_query
        final_interaction = modal.interaction

        if not query or not final_interaction:
            return

        try:

            # Fetch the data returned from the query using the service class
            lat, long = await self.api_service.fetch_lat_long(query)

            # Split up what originally gets used for the API by commas
            query_split = query.split(",")

            # Depending on if a state gets passed in or not, make sure to format the
            # queried information
            if query_split[1] == "":
                city_state_country = query_split[0] + ", " + query_split[2]
            else:
                city_state_country = (
                    query_split[0] + ", " + query_split[1] + ", " + query_split[2]
                )

            # If there was no result for the city/state/country entered, initialize the
            # following embedded message
            if lat == 0.0:
                embed = discord.Embed(
                    title=f"No Result for *{city_state_country}*",
                    color=discord.Color.dark_purple(),
                )

            # Otherwise, setup the embedded message to the have the needed information before
            # sending it
            else:

                # Create the formatted message that the bot is going to use
                message_desc = (
                    "**Lat:** *" + str(lat) + "*\n**Long**: *" + str(long) + "*"
                )

                # Create an embedded discord object that stores the information from the query
                embed = discord.Embed(
                    title=f"Result for {city_state_country}",
                    description=message_desc,
                    color=discord.Color.dark_purple(),
                )
            # Have the bot send the embedded object message to the discord chat
            await final_interaction.followup.send(embed=embed, ephemeral=True)
        except aiohttp.ClientConnectorError:

            # If an error occurred
            await final_interaction.followup.send("A connection error has occurred")


# Asynchoronous function used to add the cog to the bot


async def setup(bot: Colbot) -> None:
    """
    Function docstring placeholder
    """
    await bot.add_cog(APICog(bot))
