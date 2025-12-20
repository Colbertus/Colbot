"""
Module meant to initialize 'Colbot' along with loading its' extensions.

This module contains the primary logic for the Colbot discord client,
including custom command handling and automated event listeners.
It utilizes the discord.py library as its base.

Attributes:
    TOKEN (str): String token identifier needed to start the bot on Discord.
    ID (int): Server ID needed to refresh '/' commands on Discord.
    intents (discord.Intents): Discord object that defines what the bot can/cannot do.
    bot (Colbot): Discord object that gets created from Colbot class that uses the 'intents' object above.
    initial_extensions (list[str]): List containing the scripts that need to be connected to
        the bot on startup.
    test_guild (discord.Object): Discord object that contains the ID of my discord server for testing.
"""

# Needed Imports
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from fastapi import HTTPException


class Colbot(commands.Bot):
    """
    Class derived from 'commands.Bot' to initialize a 'bot' object.
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
    print("Bot token loaded successfully!")

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
    Asynchronous function meant to prepare the bot to start receiving commands.

    Raises:
        commands.ExtensionNotFound: If a certain python script could not be loaded in as an extension.
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
    Command function for syncing the '/' commands with Discord.

    Args:
        ctx (commands.Context): Context object that the bot uses to send messages amongst other things.

    Raises:
        HTTPException: If syncing the commands failed.
        discord.HTTPException: If the synced message failed to send.
    """

    try:
        # Sync the commands and have the bot send out how many synced commands there are
        fmt = await ctx.bot.tree.sync(guild=test_guild)
        await ctx.send(f"Synced {len(fmt)} commands to the current server")
    except HTTPException:
        print("Failed to sync commands to {test_guild}.")
    except discord.HTTPException:
        print("Failed to send message to {ctx}.")


if __name__ == "__main__":
    # Run the bot inside of an event loop that waits for commands
    bot.run(TOKEN)
