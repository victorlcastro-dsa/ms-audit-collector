import requests
import pandas as pd
from io import StringIO
from config import Config
from auth import TokenManager
from util import DataFilter
import logging

logger = logging.getLogger(__name__)

def get_sharepoint_user_activity_logs():
    access_token = TokenManager().get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    response = requests.get(Config.ENDPOINT_USER_ACTIVITY, headers=headers)

    if response.status_code == 403:
        logger.error("🚨 ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD.")
        raise Exception("🚨 ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD.")

    response.raise_for_status()

    # The API data is returned as CSV
    csv_data = response.text
    user_activity_df = pd.read_csv(StringIO(csv_data))
    return DataFilter.filter_user_activity(user_activity_df)