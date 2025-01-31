import pandas as pd
from config import Config

def simplify_user_info(user_info):
    if 'email' in user_info:
        return user_info['email']
    return user_info.get('displayName', '')

def extract_child_count(folder_info):
    if isinstance(folder_info, dict):
        return folder_info.get('childCount', 0)
    return 0

def extract_parent_name(parent_info):
    if isinstance(parent_info, dict):
        return parent_info.get('name', '')
    return ''

def filter_user_activity(user_activity_df):
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

def filter_drives(drives_df):
    columns = ["createdDateTime", "lastModifiedDateTime", "name", "webUrl"]
    return drives_df[columns]

def filter_folders(folders_df):
    columns = [
        "createdBy", "createdDateTime", "lastModifiedBy",
        "lastModifiedDateTime", "name", "webUrl", "folder", "size"
    ]
    folders_df['createdBy'] = folders_df['createdBy'].apply(lambda x: simplify_user_info(x['user']))
    folders_df['lastModifiedBy'] = folders_df['lastModifiedBy'].apply(lambda x: simplify_user_info(x['user']))
    folders_df['folder'] = folders_df['folder'].apply(extract_child_count)
    return folders_df[columns]

def filter_subfolders(subfolders_df):
    columns = [
        "createdBy", "createdDateTime", "lastModifiedBy",
        "name", "parentReference", "webUrl", "folder", "size"
    ]
    subfolders_df['createdBy'] = subfolders_df['createdBy'].apply(lambda x: simplify_user_info(x['user']))
    subfolders_df['lastModifiedBy'] = subfolders_df['lastModifiedBy'].apply(lambda x: simplify_user_info(x['user']))
    subfolders_df['folder'] = subfolders_df['folder'].apply(extract_child_count)
    subfolders_df['parentReference'] = subfolders_df['parentReference'].apply(extract_parent_name)
    return subfolders_df[columns]