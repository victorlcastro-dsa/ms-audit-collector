from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    AUTHORITY = os.getenv("AUTHORITY")
    SCOPE = [os.getenv("SCOPE")]
    ENDPOINT_USER_ACTIVITY = os.getenv("ENDPOINT_USER_ACTIVITY")