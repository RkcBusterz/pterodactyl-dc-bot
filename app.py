import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="ptero", intents=intents)

def load_cogs():
    try:
        bot.load_extension("cogs.admin")
        print("Loaded cog: admin")
    except Exception as e:
        print(f"Failed to load cog 'admin': {e}")

@bot.event
async def on_ready():
    load_cogs()
    print(f"Logged in as {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
