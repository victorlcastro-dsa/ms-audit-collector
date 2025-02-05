from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    AUTHORITY = os.getenv("AUTHORITY")
    SCOPE = [os.getenv("SCOPE")]
    SEARCH_QUERY_PATH = os.getenv("SEARCH_QUERY_PATH")
    SEARCH_QUERY_SIZE = int(os.getenv("SEARCH_QUERY_SIZE", 500))
    SEARCH_QUERY_REGION = os.getenv("SEARCH_QUERY_REGION")
    EMAIL_FILTER_LIST = os.getenv("EMAIL_FILTER_LIST").split(',')
    TOKEN_EXPIRY_BUFFER = int(os.getenv("TOKEN_EXPIRY_BUFFER", 60))
    USER_ACTIVITY_SHEET = os.getenv("USER_ACTIVITY_SHEET", "User Activity")
    DRIVES_SHEET = os.getenv("DRIVES_SHEET", "Drives")
    FOLDERS_SHEET = os.getenv("FOLDERS_SHEET", "Folders")
    SUBFOLDERS_SHEET = os.getenv("SUBFOLDERS_SHEET", "Subfolders")
    UPLOAD_FILES_SHEET = os.getenv("UPLOAD_FILES_SHEET", "Upload Files")
    FILENAME = os.getenv("FILENAME", "Audit_Accounts_Receivable.xlsx")
    LOG_FILENAME = os.getenv("LOG_FILENAME", "app.log")
    SHAREPOINT_HOST = os.getenv("SHAREPOINT_HOST")
    SHAREPOINT_SITE = os.getenv("SHAREPOINT_SITE")
    DRIVE_NAME = os.getenv("DRIVE_NAME")
    SEARCH_DATE = os.getenv("SEARCH_DATE")
    USER_ACTIVITY_PERIOD = os.getenv("USER_ACTIVITY_PERIOD", "D7")
    AUDIT_QUERY_DISPLAY_NAME = os.getenv(
        "AUDIT_QUERY_DISPLAY_NAME", "File Access Audit")
    AUDIT_QUERY_START_DATE = os.getenv(
        "AUDIT_QUERY_START_DATE", "2025-01-30T00:00:00")
    AUDIT_QUERY_END_DATE = os.getenv(
        "AUDIT_QUERY_END_DATE", "2025-01-31T00:00:00")
    AUDIT_QUERY_RECORD_TYPE_FILTERS = os.getenv(
        "AUDIT_QUERY_RECORD_TYPE_FILTERS", "sharePointFileOperation").split(',')
    AUDIT_QUERY_MONITOR_INTERVAL = int(
        os.getenv("AUDIT_QUERY_MONITOR_INTERVAL", 10))
    AUDIT_QUERY_SUCCESS_STATUS = os.getenv(
        "AUDIT_QUERY_SUCCESS_STATUS", "succeeded")
    AUDIT_QUERY_RUNNING_STATUS = os.getenv(
        "AUDIT_QUERY_RUNNING_STATUS", "running")
    AUDIT_QUERY_NOT_STARTED_STATUS = os.getenv(
        "AUDIT_QUERY_NOT_STARTED_STATUS", "notStarted")
    AUDIT_SHEET = os.getenv("AUDIT_SHEET", "Audit")
