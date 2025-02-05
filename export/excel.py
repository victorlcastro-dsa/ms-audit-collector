import pandas as pd
import xlsxwriter
import logging
from util import DataFilter
from service import SharePointUploadService
from config import Config

logger = logging.getLogger(__name__)


class AuditLogExporter:
    def __init__(self, filename: str = Config.FILENAME):
        self.filename = filename
        logging.basicConfig(level=logging.INFO)

    def save_audit_logs_to_excel(self, user_activity_logs: pd.DataFrame, drives: list, folders: list, subfolders: list, upload_files: dict, audit_logs: pd.DataFrame = None):
        with pd.ExcelWriter(self.filename, engine="xlsxwriter") as writer:
            self._save_user_activity_logs(writer, user_activity_logs)
            self._save_drives(writer, drives)
            self._save_folders(writer, folders)
            self._save_subfolders(writer, subfolders)
            self._save_upload_files(writer, upload_files)
            if audit_logs is not None:
                self._save_audit_logs(writer, audit_logs)
        logger.info("Audit saved in: %s", self.filename)

    def _save_user_activity_logs(self, writer: pd.ExcelWriter, user_activity_logs: pd.DataFrame):
        user_activity_df = DataFilter.filter_user_activity(
            pd.DataFrame(user_activity_logs))
        self._write_to_excel(writer, user_activity_df,
                             Config.USER_ACTIVITY_SHEET)

    def _save_drives(self, writer: pd.ExcelWriter, drives: list):
        drives_df = DataFilter.filter_drives(pd.DataFrame(drives))
        self._write_to_excel(writer, drives_df, Config.DRIVES_SHEET)

    def _save_folders(self, writer: pd.ExcelWriter, folders: list):
        folders_df = DataFilter.filter_folders(pd.DataFrame(folders))
        self._write_to_excel(writer, folders_df, Config.FOLDERS_SHEET)

    def _save_subfolders(self, writer: pd.ExcelWriter, subfolders: list):
        subfolders_df = DataFilter.filter_subfolders(pd.DataFrame(subfolders))
        self._write_to_excel(writer, subfolders_df, Config.SUBFOLDERS_SHEET)

    def _save_upload_files(self, writer: pd.ExcelWriter, upload_files: dict):
        upload_files_df = SharePointUploadService.process_hits_response(
            upload_files)
        self._write_to_excel(writer, upload_files_df,
                             Config.UPLOAD_FILES_SHEET)

    def _save_audit_logs(self, writer: pd.ExcelWriter, audit_logs: pd.DataFrame):
        audit_logs_df = DataFilter.filter_audit_logs(audit_logs)
        self._write_to_excel(writer, audit_logs_df, Config.AUDIT_SHEET)

    def _write_to_excel(self, writer: pd.ExcelWriter, df: pd.DataFrame, sheet_name: str):
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        logger.info("Data written to sheet: %s", sheet_name)
