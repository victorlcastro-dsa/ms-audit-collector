import aiohttp
from auth import TokenManager
import logging

logger = logging.getLogger(__name__)

async def get_site_id():
    access_token = await TokenManager().get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = "https://graph.microsoft.com/v1.0/sites/ssgruposrv.sharepoint.com:/sites/ContasaReceber-AGILLTDA"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            site_data = await response.json()
            return site_data['id']

async def get_drives(site_id):
    access_token = await TokenManager().get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            drives_data = await response.json()
            return drives_data['value']

async def list_folders(drive_id):
    access_token = await TokenManager().get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            folders_data = await response.json()
            return folders_data['value']