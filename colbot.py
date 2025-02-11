import discord
import os
import requests
import json 
from dotenv import load_dotenv
import mr_api as mr

# Load the environment file that contains the Colbot token
load_dotenv("token.env")

# Retrieve the token from the environment
TOKEN = os.getenv("DISCORD_TOKEN")

# This function is used to retrieve a random quote using the zenquotes api and return it
def inspo_quote():

    # Create the response using the requests.get method and the URL
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout = 10)
        response.raise_for_status()

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
            helpMessage = (
                "## Here are the Following Commands: ##\n" 
                "- `!hi`: *Colbot greets you*\n"
                "- `!inspire`: *Colbot will send you an inspirational quote*\n"
                "- `!mrGift`: *Colbot will send you each valid Marvel Rivals code"
                " that can unlock a previously locked skin for a hero along with their"
                " respective expiration dates*\n"
                "- `mrID`: *Colbot will provide a Marvel Rivals username given a valid ID*"
            )
            await message.channel.send(helpMessage)

        case _ if message.content.startswith('!hi'):
            await message.channel.send('It is I, the holy Colbot. Harbinger of Worlds...')

        case _ if message.content.startswith('!inspire'):
            quote = inspo_quote()
            await message.channel.send(quote)
        
        case _ if message.content.startswith('!mrGift'):
            gift = mr.gift_codes()
            await message.channel.send(gift)

        case _ if message.content.startswith('!mrID'):
            arguments = message.content.split()

            if len(arguments) != 2:
                await message.channel.send('Usage:\n  Need to provide the command along with the one argument that is required\n  Example usage: !mrID {user name}')
                return
            
            username = arguments[1]

            playerID = mr.player_id(username)
            await message.channel.send(playerID)
        
        case _ if message.content.startswith('!mrStats'):
            arguments = message.content.split()

            if len(arguments) != 2:
                usageStatement = (
                    "Usage:\n  Need to provide the command along with the one"
                    " argument that is required\n"  
                    "Example usage: !mrStats {player ID}\nOR\n"
                    "Example usage: !mrStats {user name}"
                )
                await message.channel.send(usageStatement)

            ID = arguments[1]

            if any(char.isalpha() for char in ID):
                idInfo = mr.player_id(ID)
                arguments = idInfo.split()
                actualID = arguments[3]
                stats = mr.player_stats(actualID)
                await message.channel.send(stats)
            else:
                stats = mr.player_stats(ID)
                await message.channel.send(stats)

        case _ if message.content.startswith('!mrChar'):
            
            arguments = message.content.split()

            if len(arguments) < 2:
                usageStatement = mr.character_names()
                await message.channel.send(usageStatement)
                return
            
            character = " ".join(arguments[1:])

            stats = mr.character_stats(character)

            await message.channel.send(stats)
        

client.run(TOKEN)
