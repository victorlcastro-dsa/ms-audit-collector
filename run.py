from service import get_sharepoint_user_activity_logs, get_site_id, get_drives, list_folders, list_subfolders, search_files_by_creation_date
from export import AuditLogExporter
from config import Config
from log import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class AuditCollector:
    def __init__(self):
        self.config = Config()
        self.exporter = AuditLogExporter()

    def collect_and_export_audit_logs(self):
        logger.info("📊 Collecting SharePoint activity logs...")
        user_activity_df = get_sharepoint_user_activity_logs()

        if user_activity_df.empty:
            logger.error("🚨 No audit data found!")
            return

        site_id = self._get_site_id()
        drives = self._get_drives(site_id)
        contas_a_receber_drive_id = self._get_drive_id(drives, 'Contas a Receber')
        folders = self._list_folders(contas_a_receber_drive_id)
        subfolders = self._list_all_subfolders(contas_a_receber_drive_id, folders)
        upload_files = self._search_files_by_creation_date("2025-01-30", contas_a_receber_drive_id)

        self.exporter.save_audit_logs_to_excel(user_activity_df, drives, folders, subfolders, upload_files)

    def _get_site_id(self):
        return get_site_id()

    def _get_drives(self, site_id):
        return get_drives(site_id)

    def _get_drive_id(self, drives, drive_name):
        return next(drive['id'] for drive in drives if drive['name'] == drive_name)

    def _list_folders(self, drive_id):
        return list_folders(drive_id)

    def _list_all_subfolders(self, drive_id, folders):
        subfolders = []
        for folder in folders:
            subfolders.extend(list_subfolders(drive_id, folder['id']))
        return subfolders

    def _search_files_by_creation_date(self, date, drive_id):
        return search_files_by_creation_date(date, drive_id)

# 🔹 Running Audit
if __name__ == "__main__":
    collector = AuditCollector()
    collector.collect_and_export_audit_logs()