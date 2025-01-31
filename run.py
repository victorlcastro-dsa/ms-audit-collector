from service import get_sharepoint_user_activity_logs, get_site_id, get_drives, list_folders, list_subfolders, search_files_by_creation_date
from export import AuditLogExporter
from config import Config
from log import setup_logging
import logging
import asyncio

setup_logging()
logger = logging.getLogger(__name__)

class AuditCollector:
    def __init__(self):
        self.config = Config()
        self.exporter = AuditLogExporter()

    async def collect_and_export_audit_logs(self):
        logger.info("📊 Collecting SharePoint activity logs...")
        user_activity_df = await get_sharepoint_user_activity_logs()

        if user_activity_df.empty:
            logger.error("🚨 No audit data found!")
            return

        site_id = await self._get_site_id()
        drives = await self._get_drives(site_id)
        contas_a_receber_drive_id = self._get_drive_id(drives, 'Contas a Receber')
        folders = await self._list_folders(contas_a_receber_drive_id)
        subfolders = await self._list_all_subfolders(contas_a_receber_drive_id, folders)
        upload_files = await self._search_files_by_creation_date("2025-01-30", contas_a_receber_drive_id)

        self.exporter.save_audit_logs_to_excel(user_activity_df, drives, folders, subfolders, upload_files)

    async def _get_site_id(self):
        return await get_site_id()

    async def _get_drives(self, site_id):
        return await get_drives(site_id)

    def _get_drive_id(self, drives, drive_name):
        return next(drive['id'] for drive in drives if drive['name'] == drive_name)

    async def _list_folders(self, drive_id):
        return await list_folders(drive_id)

    async def _list_all_subfolders(self, drive_id, folders):
        tasks = [list_subfolders(drive_id, folder['id']) for folder in folders]
        subfolders = await asyncio.gather(*tasks)
        return [item for sublist in subfolders for item in sublist]

    async def _search_files_by_creation_date(self, date, drive_id):
        return await search_files_by_creation_date(date, drive_id)

# 🔹 Running Audit
if __name__ == "__main__":
    collector = AuditCollector()
    asyncio.run(collector.collect_and_export_audit_logs())