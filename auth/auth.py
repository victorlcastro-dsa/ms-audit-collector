import time
import logging
from msal import ConfidentialClientApplication
from config import Config

logger = logging.getLogger(__name__)

class AuthClient:
    def __init__(self):
        self.app = ConfidentialClientApplication(
            Config.CLIENT_ID,
            authority=Config.AUTHORITY,
            client_credential=Config.CLIENT_SECRET
        )

    def acquire_token(self):
        result = self.app.acquire_token_for_client(scopes=Config.SCOPE)
        if "access_token" in result:
            return result
        else:
            raise Exception(f"Error obtaining token: {result}")

class TokenManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._token_cache = None
            self._token_expiry = 0
            self.auth_client = AuthClient()
            self._initialized = True

    def get_access_token(self):
        if self._token_cache and time.time() < self._token_expiry:
            return self._token_cache

        try:
            result = self.auth_client.acquire_token()
            self._token_cache = result["access_token"]
            self._token_expiry = time.time() + result["expires_in"] - Config.TOKEN_EXPIRY_BUFFER
            logger.info("✅ Token obtained successfully!")
            return self._token_cache
        except Exception as e:
            logger.error(f"Error obtaining token: {e}")
            raise