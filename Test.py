import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from UserMgr import UserMgr

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
class BotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = BotClient()

@bot.tree.command(name="usrcreate", description="Create a user on the Pterodactyl panel.")
@app_commands.describe(
    email="The email of the user.",
    username="The username for the user.",
    first_name="The first name of the user.",
    last_name="The last name of the user.",
    password="The password for the user (unused).",
)
async def usrcreate(interaction: discord.Interaction, email: str, username: str, first_name: str, last_name: str, password: str):
    result = UserMgr.AddUser(email, username, first_name, last_name, password)
    if result:
        await interaction.response.send_message("User created successfully.")
    else:
        await interaction.response.send_message("Failed to create user.")

bot.run(TOKEN)
