import requests
from auth import get_access_token

def get_site_id():
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = "https://graph.microsoft.com/v1.0/sites/ssgruposrv.sharepoint.com:/sites/ContasaReceber-AGILLTDA"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        site_data = response.json()
        return site_data['id']
    else:
        response.raise_for_status()

def get_drives(site_id):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        drives_data = response.json()
        return drives_data['value']
    else:
        response.raise_for_status()

def list_folders(drive_id):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        folders_data = response.json()
        return folders_data['value']
    else:
        response.raise_for_status()