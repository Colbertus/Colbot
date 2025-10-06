import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load the environment file that contains the Colbot token
load_dotenv("token.env")

# Retrieve the token from the environment
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ERROR: Bot token was not found in .env file.")
else: 
    print("Bot token loaded successfully")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

initial_extensions = ["cog"]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}. Error {e}")


bot.run(os.getenv("DISCORD_TOKEN"))
