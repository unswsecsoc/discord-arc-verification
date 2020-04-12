import requests
from config import bot_url, bot_secret
from typing import List

_bot_headers = {
    'authorization': f"Bearer srv.{bot_secret}"
}

def _build_bot_url(path: str):
    return f"{bot_url}{path}"

def bot_add_roles(user_id: str, guild_id: str, role_ids: List[str]):
    r = requests.post(_build_bot_url("/add-roles"), json={
        'user_id': user_id, 
        'guild_id': guild_id, 
        'role_ids': role_ids
    }, headers=_bot_headers)