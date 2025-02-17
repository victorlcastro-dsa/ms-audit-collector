import logging
from io import StringIO

import aiohttp
import pandas as pd

from config import Config
from util import DataFilter

from .base_sharepoint import BaseSharePointService

logger = logging.getLogger(__name__)


class SharePointUserActivityService(BaseSharePointService):
    def __init__(self):
        super().__init__()
        self.endpoint = f"https://graph.microsoft.com/v1.0/reports/getSharePointActivityUserDetail(period='{Config.USER_ACTIVITY_PERIOD}')"

    async def fetch_user_activity_data(self, access_token: str) -> str:
        headers = await self.get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint, headers=headers) as response:
                if response.status == 403:
                    logger.error(
                        "ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD."
                    )
                    raise PermissionError(
                        "ERROR: No permission to access logs. Check if Reports.Read.All is granted in Azure AD."
                    )
                response.raise_for_status()
                return await response.text()

    def process_user_activity_data(self, csv_data: str) -> pd.DataFrame:
        user_activity_df = pd.read_csv(StringIO(csv_data))
        return DataFilter.filter_user_activity(user_activity_df)

    async def get_sharepoint_user_activity_report(self) -> pd.DataFrame:
        try:
            access_token = await self.get_access_token()
            csv_data = await self.fetch_user_activity_data(access_token)
            return self.process_user_activity_data(csv_data)
        except Exception as e:
            logger.error("ERROR: Failed to get SharePoint user activity report: %s", e)
            raise
