import aiohttp
from auth import TokenManager
import logging

logger = logging.getLogger(__name__)

class SharePointSubfolderService:
    def __init__(self):
        self.token_manager = TokenManager()

    async def get_access_token(self):
        return await self.token_manager.get_access_token()

    async def list_subfolders(self, drive_id, item_id):
        access_token = await self.get_access_token()
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