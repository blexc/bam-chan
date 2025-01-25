import os
import discord
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Create global variable for LLM
LM = None

# Create global variable for Database
DB = None

# Create a new Discord client
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)

# Run the bot
client.run(os.getenv('DISCORD_BOT_TOKEN'))  # Load the bot token from the environment variable