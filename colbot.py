"""
Module Docstring Placeholder
"""

# Needed Imports
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


class Colbot(commands.Bot):
    """
    Class docstring placeholder
    """

    def __init__(self, bot_intents: discord.Intents) -> None:
        super().__init__(command_prefix="!", intents=bot_intents)


# Load the environment file that contains the Colbot token
load_dotenv("token.env")

# Retrieve the token and the server guild ID from the env file
TOKEN: str = os.getenv("DISCORD_TOKEN", "0")
ID = int(os.getenv("TEST_SERVER_ID", "0"))

# If the token is not present in the '.env' file
if not TOKEN:
    print("ERROR: Bot token was not found in .env file.")

else:
    print("Bot token loaded successfully")

# Need to set the bot's intentions to the default while setting message conent to 'True', meaning
# that the bot can send readable messages
intents = discord.Intents.default()
intents.message_content = True


# Initialize the command prefix to '!' while setting the intents
bot = Colbot(intents)

# Set 'cog.py' to be the module loaded when starting the bot
initial_extensions = ["cog"]

# Setup the guild in which we are using the slash commands in (TEMP)
test_guild = discord.Object(id=ID)


@bot.event
async def on_ready() -> None:
    """
    Function Docstring Placeholder
    """

    # Print out a debug login message once the bot connects
    print(f"We have logged in as {bot.user}")

    # Load each extension from the list from above
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except commands.ExtensionNotFound:
            print("Failed to load extension {extension}.")
    return None


# The following command will allow one to resync the slash commands in order to update the
# server for debugging purposes
@bot.command()
async def syncmds(ctx: commands.Context[Colbot]) -> None:
    """
    Function Docstring Placeholder
    """
    # Sync the commands and have the bot send out how many synced commands there are
    fmt = await ctx.bot.tree.sync(guild=test_guild)
    await ctx.send(f"Synced {len(fmt)} commands to the current server")


if __name__ == "__main__":
    # Run the bot inside of an event loop that waits for commands
    bot.run(TOKEN)
