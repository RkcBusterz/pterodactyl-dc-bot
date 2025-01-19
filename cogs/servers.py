import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
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





async def setup(bot):
    servers = await list_servers()
    print(servers)
    await bot.add_cog(AdminCog(bot))