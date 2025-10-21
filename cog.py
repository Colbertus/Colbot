# Imports
import discord
from discord.ext import commands
from discord import app_commands
from service import APIService
from weathermodal import WeatherModal
from dotenv import load_dotenv
import os

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
       
        modal = WeatherModal(cog_instance = self)
        await interaction.response.send_modal(modal)

    @app_commands.command(name = 'test')
    async def command_test(self, ctx: discord.Interaction):
        message = "Sending a test message"
        await ctx.response.send_message(message)

    # This is the command for retrieving data from OpenWeather (will get new name soon)
    async def output_lat_long(self, ctx: discord.Interaction, query: str):

        try:

            # Fetch the data returned from the query using the service class
            lat, long = await self.api_service.fetch_lat_long(query)

            querySplit = query.split(",")
            if querySplit[1] == "":
                cityStateCountry = querySplit[0] + ", " + querySplit[2]
            else:
                cityStateCountry = querySplit[0] + ", " + querySplit[1] + ", " + querySplit[2]

            if lat == None:

                embed = discord.Embed(
                    title = f"No Result for *{cityStateCountry}*",
                    color = discord.Color.dark_purple()
                )

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
            await ctx.response.send_message(embed = embed)
        except Exception as e:

            # If an error occurred 
            await ctx.response.send_message(f"An error occurred: {e}")
    

# Asynchoronous function used to add the cog to the bot 
async def setup(bot):
    await bot.add_cog(APICog(bot))