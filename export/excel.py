import pandas as pd
import xlsxwriter
from util.filters import filter_user_activity, filter_drives, filter_folders, filter_subfolders
from service import process_hits_response

class AuditLogExporter:
    def __init__(self, filename="Audit_Accounts_Receivable.xlsx"):
        self.filename = filename

    def save_audit_logs_to_excel(self, user_activity_logs, drives, folders, subfolders, upload_files):
        with pd.ExcelWriter(self.filename, engine="xlsxwriter") as writer:
            self._save_user_activity_logs(writer, user_activity_logs)
            self._save_drives(writer, drives)
            self._save_folders(writer, folders)
            self._save_subfolders(writer, subfolders)
            self._save_upload_files(writer, upload_files)
        print(f"✅ Audit saved in: {self.filename}")

    def _save_user_activity_logs(self, writer, user_activity_logs):
        user_activity_df = pd.DataFrame(user_activity_logs)
        user_activity_df = filter_user_activity(user_activity_df)
        user_activity_df.to_excel(writer, sheet_name="User Activity", index=False)

    def _save_drives(self, writer, drives):
        drives_df = pd.DataFrame(drives)
        drives_df = filter_drives(drives_df)
        drives_df.to_excel(writer, sheet_name="Drives", index=False)

    def _save_folders(self, writer, folders):
        folders_df = pd.DataFrame(folders)
        folders_df = filter_folders(folders_df)
        folders_df.to_excel(writer, sheet_name="Folders", index=False)

    def _save_subfolders(self, writer, subfolders):
        subfolders_df = pd.DataFrame(subfolders)
        subfolders_df = filter_subfolders(subfolders_df)
        subfolders_df.to_excel(writer, sheet_name="Subfolders", index=False)

    def _save_upload_files(self, writer, upload_files):
        upload_files_df = process_hits_response(upload_files)
        upload_files_df.to_excel(writer, sheet_name="Upload Files", index=False)