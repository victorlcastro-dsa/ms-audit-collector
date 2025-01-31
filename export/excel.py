import pandas as pd
import xlsxwriter
import logging
from util.filters import filter_user_activity, filter_drives, filter_folders, filter_subfolders
from service import process_hits_response

class AuditLogExporter:
    USER_ACTIVITY_SHEET = "User Activity"
    DRIVES_SHEET = "Drives"
    FOLDERS_SHEET = "Folders"
    SUBFOLDERS_SHEET = "Subfolders"
    UPLOAD_FILES_SHEET = "Upload Files"

    def __init__(self, filename: str = "Audit_Accounts_Receivable.xlsx"):
        self.filename = filename
        logging.basicConfig(level=logging.INFO)

    def save_audit_logs_to_excel(self, user_activity_logs: pd.DataFrame, drives: list, folders: list, subfolders: list, upload_files: dict):
        with pd.ExcelWriter(self.filename, engine="xlsxwriter") as writer:
            self._save_user_activity_logs(writer, user_activity_logs)
            self._save_drives(writer, drives)
            self._save_folders(writer, folders)
            self._save_subfolders(writer, subfolders)
            self._save_upload_files(writer, upload_files)
        logging.info(f"✅ Audit saved in: {self.filename}")

    def _save_user_activity_logs(self, writer: pd.ExcelWriter, user_activity_logs: pd.DataFrame):
        user_activity_df = filter_user_activity(pd.DataFrame(user_activity_logs))
        self._write_to_excel(writer, user_activity_df, self.USER_ACTIVITY_SHEET)

    def _save_drives(self, writer: pd.ExcelWriter, drives: list):
        drives_df = filter_drives(pd.DataFrame(drives))
        self._write_to_excel(writer, drives_df, self.DRIVES_SHEET)

    def _save_folders(self, writer: pd.ExcelWriter, folders: list):
        folders_df = filter_folders(pd.DataFrame(folders))
        self._write_to_excel(writer, folders_df, self.FOLDERS_SHEET)

    def _save_subfolders(self, writer: pd.ExcelWriter, subfolders: list):
        subfolders_df = filter_subfolders(pd.DataFrame(subfolders))
        self._write_to_excel(writer, subfolders_df, self.SUBFOLDERS_SHEET)

    def _save_upload_files(self, writer: pd.ExcelWriter, upload_files: dict):
        upload_files_df = process_hits_response(upload_files)
        self._write_to_excel(writer, upload_files_df, self.UPLOAD_FILES_SHEET)

    def _write_to_excel(self, writer: pd.ExcelWriter, df: pd.DataFrame, sheet_name: str):
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        logging.info(f"✅ Data written to sheet: {sheet_name}")