from service.sharepoint_user_activity import get_sharepoint_user_activity_logs
from service.sharepoint_folder_activity import get_site_id, get_drives, list_folders
from service.sharepoint_subfolder_activity import list_subfolders
from service.sharepoint_user_info import get_user_info
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

        user_info_list = []
        for user in user_activity_df['UserPrincipalName']:
            user_info = get_user_info(user)
            user_info_list.append(user_info)

        save_audit_logs_to_excel(user_activity_df, {"site_id": site_id}, drives, folders, subfolders, user_info_list)