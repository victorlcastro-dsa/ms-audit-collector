from .base_sharepoint import BaseSharePointService


class SharePointSubfolderService(BaseSharePointService):
    async def list_subfolders(self, drive_id, item_id):
        access_token = await self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{
            item_id
        }/children"
        subfolders_data = await self.make_request("GET", url, headers=headers)
        return subfolders_data["value"]
