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
    SEARCH_QUERY_PATH = os.getenv("SEARCH_QUERY_PATH")
    SEARCH_QUERY_SIZE = int(os.getenv("SEARCH_QUERY_SIZE", 500))
    SEARCH_QUERY_REGION = os.getenv("SEARCH_QUERY_REGION")
    EMAIL_FILTER_LIST = os.getenv("EMAIL_FILTER_LIST").split(',')
    TOKEN_EXPIRY_BUFFER = int(os.getenv("TOKEN_EXPIRY_BUFFER", 60))