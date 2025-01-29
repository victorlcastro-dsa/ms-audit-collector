from service import get_sharepoint_user_activity_logs, get_site_id, get_drives, list_folders, list_subfolders
from export import save_audit_logs_to_excel

# 🔹 Running Audit
if __name__ == "__main__":
    print("📊 Collecting SharePoint activity logs...")
    user_activity_df = get_sharepoint_user_activity_logs()

    if user_activity_df.empty:
        print("🚨 No audit data found!")
    else:
        site_id = get_site_id()
        drives = get_drives(site_id)
        contas_a_receber_drive_id = next(drive['id'] for drive in drives if drive['name'] == 'Contas a Receber')
        folders = list_folders(contas_a_receber_drive_id)

        subfolders = []
        for folder in folders:
            subfolders.extend(list_subfolders(contas_a_receber_drive_id, folder['id']))

        save_audit_logs_to_excel(user_activity_df, drives, folders, subfolders)