import pandas as pd

def simplify_user_info(user_info):
    if 'email' in user_info:
        return user_info['email']
    return user_info.get('displayName', '')

def filter_user_activity(user_activity_df):
    columns = [
        "Report Refresh Date", "User Principal Name", "Last Activity Date",
        "Viewed Or Edited File Count", "Synced File Count",
        "Shared Internally File Count", "Shared Externally File Count",
        "Visited Page Count", "Report Period"
    ]
    return user_activity_df[columns]

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
    return folders_df[columns]

def filter_subfolders(subfolders_df):
    columns = [
        "createdBy", "createdDateTime", "lastModifiedBy",
        "name", "parentReference", "webUrl", "folder", "size"
    ]
    subfolders_df['createdBy'] = subfolders_df['createdBy'].apply(lambda x: simplify_user_info(x['user']))
    subfolders_df['lastModifiedBy'] = subfolders_df['lastModifiedBy'].apply(lambda x: simplify_user_info(x['user']))
    return subfolders_df[columns]