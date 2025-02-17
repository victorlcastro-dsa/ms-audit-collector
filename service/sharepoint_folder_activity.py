from config import Config

from .base_sharepoint import BaseSharePointService


class SharePointFolderService(BaseSharePointService):
    async def get_site_id(self):
        headers = await self.get_headers()
        url = f"https://graph.microsoft.com/v1.0/sites/{Config.SHAREPOINT_HOST}.sharepoint.com:/sites/{Config.SHAREPOINT_SITE}"
        site_data = await self.make_request("GET", url, headers=headers)
        return site_data["id"]

    async def get_drives(self, site_id):
        headers = await self.get_headers()
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        drives_data = await self.make_paginated_request("GET", url, headers=headers)
        return drives_data

    async def list_folders(self, drive_id):
        headers = await self.get_headers()
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
        folders_data = await self.make_paginated_request("GET", url, headers=headers)
        return folders_data
