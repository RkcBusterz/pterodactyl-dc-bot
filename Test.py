import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import requests
import json
from UserMgr import UserMgr

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PTERO_PANEL = os.getenv("PTERO_PANEL")
PTERO_API = os.getenv("PTERO_API")

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

    if result and 'error' not in result:
        response = requests.get(f"{PTERO_PANEL}/api/application/users", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PTERO_API}",
        })

        if response.status_code == 200:
            users = response.json()
            user_id = None
            for user in users['data']:
                if user['username'] == username:
                    user_id = user['id']
                    break
            
            if user_id:
                if not os.path.exists("Users.json"):
                    with open("Users.json", "w") as f:
                        json.dump({}, f)

                with open("Users.json", "r") as f:
                    users_data = json.load(f)

                users_data[username] = user_id

                with open("Users.json", "w") as f:
                    json.dump(users_data, f)

                embed = discord.Embed(
                    title="🎉 User Created Successfully! 🎉",
                    description=f"**Username:** {username}\n**Email:** {email}\n\nThe user has been successfully created in the Pterodactyl panel.",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ User Not Found ❌",
                    description="We couldn't find the user with the specified username after creating.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ User Creation Failed ❌",
                description=f"An error occurred while trying to retrieve the user list.\n\n**Error Message:** {response.text}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
    else:
        error_message = result.get("error", "An unexpected error occurred.")
        embed = discord.Embed(
            title="❌ User Creation Failed ❌",
            description=f"An error occurred while trying to create the user.\n\n**Error Message:** {error_message}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
