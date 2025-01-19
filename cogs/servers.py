import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import requests
import json 
url = f"{os.getenv('PTERO_PANEL')}/api/application/servers"
api_key = os.getenv("PTERO_API")
async def list_servers():
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"{response.status_code}",
            "message": response.text
        }

users = ["1319583634759614553"]

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="list_all_servers")
    async def _list(self,interaction):
        if any(item == f"{interaction.user.id}" for item in users):
            servers = await list_servers()
            list = "Name         |         Suspended \n"
            for server in servers["data"]:
                list+= f"[{server["attributes"]["name"]}     |     {server["attributes"]["suspended"]}]({os.getenv('PTERO_PANEL')}/server/{server["attributes"]["identifier"]}) \n"
            embed = discord.Embed(title="Servers of Your Panel",description=list,color=discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Who asked you to run this command ? Am I a slave ? Get lost!!!")



async def setup(bot):
    await bot.add_cog(AdminCog(bot))