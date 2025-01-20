import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import requests
import json 
import random
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


async def create_server(name,user,egg,memory,disk,cpu,docker,startup,variables):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "name": name,
        "user": user,
        "egg": egg,
        "docker_image": docker,
        "startup": startup,
        "environment": variables,
        "limits": {
            "memory": memory,
            "swap": 0,
            "disk": disk,
            "io": 500,
            "cpu": cpu
        },
        "feature_limits": {
        "databases": 0,
        "backups": 0
        },
        "allocation": {
            "default": random.randint(1, 100)

        }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text


with open('settings.json', 'r') as file:
     data = json.load(file)
     users = data["whitelisted_users"]
     eggs = data["eggs"]


class ServersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(name="list_all_servers")
    async def _list(self,interaction: discord.Interaction):
        if any(item == f"{interaction.user.id}" for item in users):
            servers = await list_servers()
            list = "Name         |         Suspended \n"
            for server in servers["data"]:
                list+= f"[{server["attributes"]["name"]}     |     {server["attributes"]["suspended"]}]({os.getenv('PTERO_PANEL')}/server/{server["attributes"]["identifier"]}) \n"
            embed = discord.Embed(title="Servers of Your Panel",description=list,color=discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Who asked you to run this command ? Am I a slave ? Get lost!!!")


    @app_commands.command(name="create_server")
    @app_commands.choices(egg=[discord.app_commands.Choice(name=key, value=key) for key in eggs.keys()])
    async def _create(self,interaction: discord.Interaction,egg: str, user: int, memory: int, cpu: int, storage: int,name: str = "Server"):
        if any(item == f"{interaction.user.id}" for item in users):
            try:
                info = eggs[f'{egg}']
                response = await create_server(name,user,info["id"],memory,storage,cpu,info["docker_image"],info["startup"],info["variables"])
                print(response)
                await interaction.response.send_message("Successfully created Server")
            except:
                await interaction.response.send_message("Unable to create server.")
        else: 
            await interaction.response.send_message("You arent authorised in my database to create any server, hardware doesnt grow on trees.")
async def setup(bot):

    await bot.add_cog(ServersCog(bot))