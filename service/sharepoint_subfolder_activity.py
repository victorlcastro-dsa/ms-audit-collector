import aiohttp
from auth import TokenManager
import logging

logger = logging.getLogger(__name__)

async def list_subfolders(drive_id, item_id):
    access_token = await TokenManager().get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/children"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            subfolders_data = await response.json()
            return subfolders_data['value']