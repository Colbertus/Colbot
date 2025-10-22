# Imports
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from service import APIService
from weathermodal import WeatherModal

# This will be temporary but serves to create the needed guild object used to sync commands faster
load_dotenv("token.env")
ID = int(os.getenv("TEST_SERVER_ID"))
test_guild = discord.Object(id = ID)

# Class used to store the commands for the OpenWeatherAPI
class APICog(commands.Cog):
    def __init__(self, bot):

        # Initialize both the bot and the API Service 
        self.bot = bot
        self.api_service = APIService()

    # Discord Command: city_lookup
    @app_commands.guilds(test_guild)
    @app_commands.command(name = "city_lookup")
    async def cityLookup(self, interaction: discord.Interaction):
        
        # Setup the modal weather object that'll be used for the query before sending it
        modal = WeatherModal(cog_instance = self)
        await interaction.response.send_modal(modal)

    # This is the command for retrieving data from OpenWeather (will get new name soon)
    # This gets used with the cityLookup function to return the lat and long of the location that gets entered 
    async def outputLatLong(self, interation: discord.Interaction, query: str):

        try:

            # Fetch the data returned from the query using the service class
            lat, long = await self.api_service.fetch_lat_long(query)

            # Split up what originally gets used for the API by commas
            querySplit = query.split(",")

            # Depending on if a state gets passed in or not, make sure to format the queried information
            if querySplit[1] == "":
                cityStateCountry = querySplit[0] + ", " + querySplit[2]
            else:
                cityStateCountry = querySplit[0] + ", " + querySplit[1] + ", " + querySplit[2]

            # If there was no result for the city/state/country entered, initialize the following embedded message
            if lat == None:
                embed = discord.Embed(
                    title = f"No Result for *{cityStateCountry}*",
                    color = discord.Color.dark_purple()
                )

            # Otherwise, setup the embedded message to the have the needed information before sending it
            else:

                # Create the formatted message that the bot is going to use
                messageDesc = (
                    "**Lat:** *" + str(lat) + "*" 
                    "\n**Long**: *" + str(long) + "*"
                )

                # Create an embedded discord object that stores the information from the query 
                embed = discord.Embed(
                    title = f"Result for {cityStateCountry}",
                    description = messageDesc,
                    color = discord.Color.dark_purple()
                )

            # Have the bot send the embedded object message to the discord chat
            await interation.response.send_message(embed = embed)
        except Exception as e:

            # If an error occurred 
            await interation.response.send_message(f"An error occurred: {e}")
    

# Asynchoronous function used to add the cog to the bot 
async def setup(bot):
    await bot.add_cog(APICog(bot))