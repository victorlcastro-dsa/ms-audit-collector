import requests
from auth import get_access_token

def get_user_info(user_principal_name):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()