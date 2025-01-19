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



class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="listall")
    async def _list(self,interaction):
        servers = await list_servers()
        list = "Name         |         Suspended \n"
        for server in servers["data"]:
            list+= f"[{server["attributes"]["name"]}     |     {server["attributes"]["suspended"]}]({os.getenv('PTERO_PANEL')}/server/{server["attributes"]["identifier"]}) \n"
        await interaction.response.send_message(list)
        # print(f"{server} \n")



async def setup(bot):
    await bot.add_cog(AdminCog(bot))