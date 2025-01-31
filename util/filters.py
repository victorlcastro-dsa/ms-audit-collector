import pandas as pd
from config import Config
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataFilter:
    @staticmethod
    def simplify_user_info(user_info: Dict[str, Any]) -> str:
        """Simplify user information to return email or display name."""
        return user_info.get('email', user_info.get('displayName', ''))

    @staticmethod
    def extract_child_count(folder_info: Dict[str, Any]) -> int:
        """Extract the child count from folder information."""
        return folder_info.get('childCount', 0) if isinstance(folder_info, dict) else 0

    @staticmethod
    def extract_parent_name(parent_info: Dict[str, Any]) -> str:
        """Extract the parent name from parent information."""
        return parent_info.get('name', '') if isinstance(parent_info, dict) else ''

    @staticmethod
    def filter_user_activity(user_activity_df: pd.DataFrame) -> pd.DataFrame:
        """Filter user activity data based on predefined columns and email filter list."""
        columns = [
            "Report Refresh Date", "User Principal Name", "Last Activity Date",
            "Viewed Or Edited File Count", "Synced File Count",
            "Shared Internally File Count", "Shared Externally File Count",
            "Visited Page Count", "Report Period"
        ]
        filtered_df = user_activity_df[columns]
        email_filter = filtered_df["User Principal Name"].str.contains(
            '|'.join(Config.EMAIL_FILTER_LIST), case=False, na=False
        )
        return filtered_df[email_filter]

    @staticmethod
    def filter_drives(drives_df: pd.DataFrame) -> pd.DataFrame:
        """Filter drives data based on predefined columns."""
        columns = ["createdDateTime", "lastModifiedDateTime", "name", "webUrl"]
        return drives_df[columns]

    @staticmethod
    def filter_folders(folders_df: pd.DataFrame) -> pd.DataFrame:
        """Filter folders data and simplify user information."""
        columns = [
            "createdBy", "createdDateTime", "lastModifiedBy",
            "lastModifiedDateTime", "name", "webUrl", "folder", "size"
        ]
        folders_df['createdBy'] = folders_df['createdBy'].apply(lambda x: DataFilter.simplify_user_info(x['user']))
        folders_df['lastModifiedBy'] = folders_df['lastModifiedBy'].apply(lambda x: DataFilter.simplify_user_info(x['user']))
        folders_df['folder'] = folders_df['folder'].apply(DataFilter.extract_child_count)
        return folders_df[columns]

    @staticmethod
    def filter_subfolders(subfolders_df: pd.DataFrame) -> pd.DataFrame:
        """Filter subfolders data and simplify user and parent information."""
        columns = [
            "createdBy", "createdDateTime", "lastModifiedBy",
            "name", "parentReference", "webUrl", "folder", "size"
        ]
        subfolders_df['createdBy'] = subfolders_df['createdBy'].apply(lambda x: DataFilter.simplify_user_info(x['user']))
        subfolders_df['lastModifiedBy'] = subfolders_df['lastModifiedBy'].apply(lambda x: DataFilter.simplify_user_info(x['user']))
        subfolders_df['folder'] = subfolders_df['folder'].apply(DataFilter.extract_child_count)
        subfolders_df['parentReference'] = subfolders_df['parentReference'].apply(DataFilter.extract_parent_name)
        return subfolders_df[columns]