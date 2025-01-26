import os
import discord
from dotenv import load_dotenv

from llama import llama_respond

# Load the environment variables from the .env file
load_dotenv()

BOT_PERSONALITY="You are an anime girl named 'Bam-chan'. Use puns relating to explosions in your response."

# Create a new Discord client
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def handle_message(message):
    if message.author == client.user:
        return

    response = llama_respond(BOT_PERSONALITY, message.content)
    await message.channel.send(response)


@client.event
async def on_message(message: discord.Message) -> None:
    # Start the message handler task in the background
    client.loop.create_task(handle_message(message))

# Run the bot
client.run(os.getenv('DISCORD_BOT_TOKEN'))  # Load the bot token from the environment variable
