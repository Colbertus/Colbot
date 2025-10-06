# Imports
import discord
from discord.ext import commands
from service import APIService

class APICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_service = APIService()

    @commands.command(name = "get_data")
    async def get_data_command(self, ctx, query: str):
        try:
            data_result = await self.api_service.fetch_data(query)

            embed = discord.Embed(
                title = f"Result for '{query}'",
                description = data_result,
                color = discord.Color.blue()
            )

            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(APICog(bot))