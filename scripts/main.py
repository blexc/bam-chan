import os
import emoji
import discord
from dotenv import load_dotenv

from llama import llama_respond
from audio import text_to_speech

from settings import allowed_channels

# Load the environment variables from the .env file
load_dotenv()

# Create a new Discord client
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)

def remove_emojis(text):
    return emoji.replace_emoji(text, replace="")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def handle_message(message):
    if message.author == client.user:
        return
    
    if client.user.mentioned_in(message) and message.channel.name in allowed_channels:
        # Remove @bam-chan from the message
        message_to_bot = message.clean_content.replace(f"@{client.user.display_name} ", "")

        # Send message and receive response
        response = llama_respond(message.author.display_name, message_to_bot)
        response = discord.utils.escape_mentions(response)

        # Generate TTS
        audio_filepath = text_to_speech(remove_emojis(response))

        # Send response back to discord channel
        await message.channel.send(response, file=discord.File(audio_filepath))

@client.event
async def on_message(message: discord.Message) -> None:
    # Start the message handler task in the background
    client.loop.create_task(handle_message(message))

# Run the bot
client.run(os.getenv('DISCORD_BOT_TOKEN'))  # Load the bot token from the environment variable
