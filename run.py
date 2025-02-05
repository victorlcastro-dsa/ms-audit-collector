from service import SharePointUserActivityService, SharePointFolderService, SharePointSubfolderService, SharePointUploadService, AuditLogQuery
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
        self.user_activity_service = SharePointUserActivityService()
        self.folder_service = SharePointFolderService()
        self.subfolder_service = SharePointSubfolderService()
        self.upload_service = SharePointUploadService()
        self.audit_log_query_service = AuditLogQuery()

    async def collect_and_export_audit_logs(self):
        logger.info("📊 Collecting SharePoint activity logs...")
        user_activity_df = await self.user_activity_service.get_sharepoint_user_activity_report()

        if user_activity_df.empty:
            logger.error("🚨 No audit data found!")
            return

        site_id = await self.folder_service.get_site_id()
        drives = await self.folder_service.get_drives(site_id)
        contas_a_receber_drive_id = self._get_drive_id(
            drives, Config.DRIVE_NAME)
        folders = await self.folder_service.list_folders(contas_a_receber_drive_id)
        subfolders = await self._list_all_subfolders(contas_a_receber_drive_id, folders)
        upload_files = await self._search_files_by_creation_date(Config.SEARCH_DATE, contas_a_receber_drive_id)

        self.exporter.save_audit_logs_to_excel(
            user_activity_logs=user_activity_df, drives=drives, folders=folders, subfolders=subfolders, upload_files=upload_files)

        audit_log_df = await self.audit_log_query_service.run_audit_log_query()
        self.exporter.save_audit_logs_to_excel(user_activity_logs=user_activity_df, drives=drives,
                                               folders=folders, subfolders=subfolders, upload_files=upload_files, audit_logs=audit_log_df)

    def _get_drive_id(self, drives, drive_name):
        return next(drive['id'] for drive in drives if drive['name'] == drive_name)

    async def _list_all_subfolders(self, drive_id, folders):
        tasks = [self.subfolder_service.list_subfolders(
            drive_id, folder['id']) for folder in folders]
        subfolders = await asyncio.gather(*tasks)
        return [item for sublist in subfolders for item in sublist]

    async def _search_files_by_creation_date(self, date, drive_id):
        return await self.upload_service.search_files_by_creation_date(date, drive_id)


# 🔹 Running Audit
if __name__ == "__main__":
    collector = AuditCollector()
    asyncio.run(collector.collect_and_export_audit_logs())
