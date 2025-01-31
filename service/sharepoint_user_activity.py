import requests
import pandas as pd
from io import StringIO
from config import Config
from auth import get_access_token
from util.filters import filter_user_activity

def get_sharepoint_user_activity_logs():
    ACCESS_TOKEN = get_access_token()
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}
    response = requests.get(Config.ENDPOINT_USER_ACTIVITY, headers=headers)

    if response.status_code == 403:
        raise Exception("🚨 ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD.")

    response.raise_for_status()

    # The API data is returned as CSV
    csv_data = response.text
    user_activity_df = pd.read_csv(StringIO(csv_data))
    return filter_user_activity(user_activity_df)