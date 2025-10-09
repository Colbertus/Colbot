# Imports
import discord
from discord.ext import commands
from discord import app_commands
from service import APIService
from weathermodel import WeatherModal

# Class used to store the commands for the OpenWeatherAPI
class APICog(commands.Cog):
    def __init__(self, bot):

        # Initialize both the bot and the API Service 
        self.bot = bot
        self.api_service = APIService()

    @app_commands.command(name = "geo_lookup")
    async def geo_lookup(self, interaction: discord.Interaction):
       
        modal = WeatherModal(cog_instance = self)
        await interaction.response.send_modal(modal)

    @app_commands.command(name = 'test')
    async def command_test(self, ctx: discord.Interaction):
        message = "Sending a test message"
        await ctx.response.send_message(message)

    # This is the command for retrieving data from OpenWeather (will be changed soon)
    async def output_lat_long(self, ctx: discord.Interaction, query: str):

        try:

            # Fetch the data returned from the query
            lat, long = await self.api_service.fetch_lat_long(query)

            querySplit = query.split(",")
            cityState = querySplit[0] + ", " + querySplit[1]

            # Create the formatted message that the bot is going to use
            messageDesc = (
                "**Lat:** *" + str(lat) + "*" 
                "\n**Long**: *" + str(long) + "*"
            )

            # Create an embedded discord object that stores the information from the query 
            embed = discord.Embed(
                title = f"Result for {cityState}",
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