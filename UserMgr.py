import os
import requests
from dotenv import load_dotenv

load_dotenv()

PTERO_PANEL = os.getenv("PTERO_PANEL")
PTERO_API = os.getenv("PTERO_API")


class UserMgr:
    @staticmethod
    def AddUser(email, username, first_name, last_name, password):
        if not PTERO_PANEL or not PTERO_API:
            return False

        url = f"{PTERO_PANEL}/api/application/users"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PTERO_API}",
        }
        body = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }

        try:
            response = requests.post(url, json=body, headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def DeleteUser(user_id):
        if not PTERO_PANEL or not PTERO_API:
            return False

        url = f"{PTERO_PANEL}/api/application/users/{user_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PTERO_API}",
        }

        try:
            response = requests.delete(url, headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
