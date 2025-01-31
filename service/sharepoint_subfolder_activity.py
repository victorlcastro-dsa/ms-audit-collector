import requests
from auth import TokenManager

def list_subfolders(drive_id, item_id):
    access_token = TokenManager().get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/children"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        subfolders_data = response.json()
        return subfolders_data['value']
    else:
        response.raise_for_status()