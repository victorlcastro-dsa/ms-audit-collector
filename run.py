from service import get_sharepoint_activity_logs
from util import process_activity_logs
from export import save_audit_logs_to_excel

# 🔹 Running Audit
if __name__ == "__main__":
    print("📊 Collecting SharePoint activity logs...")
    df = get_sharepoint_activity_logs()

    if df.empty:
        print("🚨 No audit data found!")
    else:
        processed_logs = process_activity_logs(df)
        save_audit_logs_to_excel(processed_logs)