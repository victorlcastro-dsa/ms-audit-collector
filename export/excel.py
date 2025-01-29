import pandas as pd
import xlsxwriter
from util.filters import filter_user_activity, filter_drives, filter_folders, filter_subfolders

def save_audit_logs_to_excel(user_activity_logs, drives, folders, subfolders):
    writer = pd.ExcelWriter("Audit_Accounts_Receivable.xlsx", engine="xlsxwriter")

    # Save user activity logs
    user_activity_df = pd.DataFrame(user_activity_logs)
    user_activity_df = filter_user_activity(user_activity_df)
    user_activity_df.to_excel(writer, sheet_name="User Activity", index=False)

    # Save drives
    drives_df = pd.DataFrame(drives)
    drives_df = filter_drives(drives_df)
    drives_df.to_excel(writer, sheet_name="Drives", index=False)

    # Save folders
    folders_df = pd.DataFrame(folders)
    folders_df = filter_folders(folders_df)
    folders_df.to_excel(writer, sheet_name="Folders", index=False)

    # Save subfolders
    subfolders_df = pd.DataFrame(subfolders)
    subfolders_df = filter_subfolders(subfolders_df)
    subfolders_df.to_excel(writer, sheet_name="Subfolders", index=False)

    writer.close()
    print("✅ Audit saved in: Audit_Accounts_Receivable.xlsx")