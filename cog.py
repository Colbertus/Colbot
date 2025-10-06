# Imports
import discord
from discord.ext import commands
from service import APIService

# Class used to store the commands for the OpenWeatherAPI
class APICog(commands.Cog):
    def __init__(self, bot):

        # Initialize both the bot and the API Service 
        self.bot = bot
        self.api_service = APIService()

    # This is the command for retrieving data from OpenWeather (will be changed soon)
    @commands.command(name = "get_data")
    async def get_data_command(self, ctx, query: str):
        try:

            # Fetch the data returned from the query
            data_result = await self.api_service.fetch_data(query)

            # Create an embedded discord object that stores the information from the query 
            embed = discord.Embed(
                title = f"Result for '{query}'",
                description = data_result,
                color = discord.Color.dark_purple()
            )

            # Have the bot send the embedded object message to the discord chat
            await ctx.send(embed = embed)
        except Exception as e:

            # If an error occurred 
            await ctx.send(f"An error occurred: {e}")

# Asynchoronous function used to add the cog to the bot 
async def setup(bot):
    await bot.add_cog(APICog(bot))