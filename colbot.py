import discord
import os
from dotenv import load_dotenv

load_dotenv("token.env")

TOKEN = os.getenv("DISCORD_TOKEN")


if not TOKEN:
    print("ERROR: Bot token was not found in .env file.")
else: 
    print("Bot token loaded successfully")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.content.startswith('Colbot'):
        await message.channel.send('It is I, the holy Colbot. Harbinger of Worlds...')

client.run(TOKEN)
