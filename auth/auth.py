from msal import ConfidentialClientApplication
from config import Config

def get_access_token():
    app = ConfidentialClientApplication(Config.CLIENT_ID, authority=Config.AUTHORITY, client_credential=Config.CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=Config.SCOPE)
    if "access_token" in result:
        print("✅ Token obtained successfully!")
        return result["access_token"]
    else:
        raise Exception(f"Error obtaining token: {result}")