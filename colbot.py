import discord
import os
import requests
import json 
from dotenv import load_dotenv

# Load the environment file that contains the Colbot token
load_dotenv("token.env")

# Retrieve the token from the environment
TOKEN = os.getenv("DISCORD_TOKEN")

# This function is used to retrieve a random quote using the zenquotes api and return it
def inspo_quote():

    # Create the response using the requests.get method and the URL
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout = 10)

        # Save the JSON array that gets downloaded from the API call
        json_data = json.loads(response.text)

        # Fix the struture and formatting of the quote and return it
        quote = json_data[0]['q'] + "\n  -" + json_data[0]['a']
        return quote
    except requests.exceptions.RequestException as e:
        error = f"An error occurred: {e}"
        return error 

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


    match True: 

        case _ if message.content == 'help':
            await message.channel.send('Here are the following commands: \n  !hi: Colbot greets you\n  !inspire: Colbot will send you an inspirational quote')
        case _ if message.content.startswith('!hi'):
            await message.channel.send('It is I, the holy Colbot. Harbinger of Worlds...')

        case _ if message.content.startswith('!inspire'):
            quote = inspo_quote()
            await message.channel.send(quote)

client.run(TOKEN)
