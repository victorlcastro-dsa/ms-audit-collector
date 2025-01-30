from msal import ConfidentialClientApplication
from config import Config
import time

_token_cache = None
_token_expiry = 0

def get_access_token():
    global _token_cache, _token_expiry
    if _token_cache and time.time() < _token_expiry:
        return _token_cache

    app = ConfidentialClientApplication(Config.CLIENT_ID, authority=Config.AUTHORITY, client_credential=Config.CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=Config.SCOPE)
    if "access_token" in result:
        _token_cache = result["access_token"]
        _token_expiry = time.time() + result["expires_in"] - 60  # Subtract 60 seconds to account for clock skew
        print("✅ Token obtained successfully!")
        return _token_cache
    else:
        raise Exception(f"Error obtaining token: {result}")