import pandas as pd
import xlsxwriter

def save_audit_logs_to_excel(user_activity_logs, site_info, drives, folders, subfolders, user_info_list):
    writer = pd.ExcelWriter("Audit_Accounts_Receivable.xlsx", engine="xlsxwriter")

    # Save user activity logs
    user_activity_df = pd.DataFrame(user_activity_logs)
    user_activity_df.to_excel(writer, sheet_name="User Activity", index=False)

    # Save site info
    site_info_df = pd.DataFrame([site_info])
    site_info_df.to_excel(writer, sheet_name="Site Info", index=False)

    # Save drives
    drives_df = pd.DataFrame(drives)
    drives_df.to_excel(writer, sheet_name="Drives", index=False)

    # Save folders
    folders_df = pd.DataFrame(folders)
    folders_df.to_excel(writer, sheet_name="Folders", index=False)

    # Save subfolders
    subfolders_df = pd.DataFrame(subfolders)
    subfolders_df.to_excel(writer, sheet_name="Subfolders", index=False)

    # Save user info
    user_info_df = pd.DataFrame(user_info_list)
    user_info_df.to_excel(writer, sheet_name="User Info", index=False)

    writer.close()
    print("✅ Audit saved in: Audit_Accounts_Receivable.xlsx")