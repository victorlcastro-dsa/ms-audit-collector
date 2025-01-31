import aiohttp
import pandas as pd
from io import StringIO
from config import Config
from auth import TokenManager
from util import DataFilter
import logging

logger = logging.getLogger(__name__)

async def get_sharepoint_user_activity_logs():
    access_token = await TokenManager().get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(Config.ENDPOINT_USER_ACTIVITY, headers=headers) as response:
            if response.status == 403:
                logger.error("🚨 ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD.")
                raise Exception("🚨 ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD.")
            response.raise_for_status()
            csv_data = await response.text()
            user_activity_df = pd.read_csv(StringIO(csv_data))
            return DataFilter.filter_user_activity(user_activity_df)