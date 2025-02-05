import aiohttp
import asyncio
import logging
import pandas as pd
from datetime import datetime
from typing import List, Optional
from config import Config
from service.base_sharepoint import BaseSharePointService

logger = logging.getLogger(__name__)


class AuditLogQuery(BaseSharePointService):
    async def create_audit_query(
        self,
        display_name: str,
        start_date: datetime,
        end_date: datetime,
        record_type_filters: Optional[List[str]] = None,
        operation_filters: Optional[List[str]] = None,
        user_principal_name_filters: Optional[List[str]] = None,
        ip_address_filters: Optional[List[str]] = None,
        object_id_filters: Optional[List[str]] = None,
        administrative_unit_id_filters: Optional[List[str]] = None,
        keyword_filter: Optional[str] = None,
        service_filter: Optional[str] = None
    ) -> dict:
        access_token = await self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        url = "https://graph.microsoft.com/beta/security/auditLog/queries"
        payload = {
            "displayName": display_name,
            "filterStartDateTime": start_date.isoformat(),
            "filterEndDateTime": end_date.isoformat(),
            "recordTypeFilters": record_type_filters or [],
            "operationFilters": operation_filters or [],
            "userPrincipalNameFilters": user_principal_name_filters or [],
            "ipAddressFilters": ip_address_filters or [],
            "objectIdFilters": object_id_filters or [],
            "administrativeUnitIdFilters": administrative_unit_id_filters or [],
            "keywordFilter": keyword_filter,
            "serviceFilter": service_filter
        }
        payload = {k: v for k, v in payload.items() if v}
        logger.debug(f"Sending request to {url} with payload: {payload}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return await response.json()

    async def get_audit_query_status(self, audit_log_query_id: str) -> dict:
        access_token = await self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        url = f"https://graph.microsoft.com/beta/security/auditLog/queries/{
            audit_log_query_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    async def get_audit_query_results(self, audit_log_query_id: str) -> dict:
        access_token = await self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        url = f"https://graph.microsoft.com/beta/security/auditLog/queries/{
            audit_log_query_id}/records"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    async def monitor_audit_query(self, audit_log_query_id: str):
        while True:
            status_response = await self.get_audit_query_status(audit_log_query_id)
            status = status_response.get('status')
            logger.info(f"Audit query status: {status}")
            if status in [Config.AUDIT_QUERY_SUCCESS_STATUS]:
                return
            elif status in [Config.AUDIT_QUERY_NOT_STARTED_STATUS, Config.AUDIT_QUERY_RUNNING_STATUS]:
                await asyncio.sleep(Config.AUDIT_QUERY_MONITOR_INTERVAL)
            else:
                raise Exception(f"Unexpected status: {status}")

    async def run_audit_log_query(self) -> pd.DataFrame:
        start_date = datetime.fromisoformat(Config.AUDIT_QUERY_START_DATE)
        end_date = datetime.fromisoformat(Config.AUDIT_QUERY_END_DATE)
        query_response = await self.create_audit_query(
            display_name=Config.AUDIT_QUERY_DISPLAY_NAME,
            start_date=start_date,
            end_date=end_date,
            record_type_filters=Config.AUDIT_QUERY_RECORD_TYPE_FILTERS,
            object_id_filters=[f"https://{Config.SHAREPOINT_HOST}.sharepoint.com/sites/{
                Config.SHAREPOINT_SITE}/{Config.DRIVE_NAME}"]
        )
        audit_log_query_id = query_response['id']
        await self.monitor_audit_query(audit_log_query_id)
        results = await self.get_audit_query_results(audit_log_query_id)
        return pd.DataFrame(results['value'])
