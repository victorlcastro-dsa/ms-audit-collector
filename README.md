# ms-audit-collector

`Under Development`

## Overview

The ms-audit-collector project is designed to collect and export SharePoint activity logs. It utilizes the Microsoft Graph API to query audit logs, fetch user activity, and retrieve folder and file information from SharePoint. The collected data is processed and saved into an Excel file using pandas and xlsxwriter. The project includes configuration management, logging setup, and token-based authentication.

## Features

- **SharePoint User Activity Logs**: Collects user activity logs from SharePoint.
- **Folder and Subfolder Information**: Retrieves information about folders and subfolders in SharePoint.
- **File Upload Activity**: Tracks file upload activities in SharePoint.
- **Audit Log Queries**: Executes and monitors audit log queries using Microsoft Graph API.
- **Excel Export**: Exports the collected data into an Excel file with multiple sheets.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/victorlcastro-dsa/ms-audit-collector.git
    cd ms-audit-collector
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add the necessary environment variables:
    ```env
    TENANT_ID=your_tenant_id
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    AUTHORITY=https://login.microsoftonline.com/your_tenant_id
    SCOPE=https://graph.microsoft.com/.default
    SEARCH_QUERY_PATH=your_search_query_path
    SEARCH_QUERY_SIZE=500
    SEARCH_QUERY_REGION=your_search_query_region
    EMAIL_FILTER_LIST=email1@example.com,email2@example.com
    TOKEN_EXPIRY_BUFFER=60
    USER_ACTIVITY_SHEET=User Activity
    DRIVES_SHEET=Drives
    FOLDERS_SHEET=Folders
    SUBFOLDERS_SHEET=Subfolders
    UPLOAD_FILES_SHEET=Upload Files
    FILENAME=Audit_Accounts_Receivable.xlsx
    LOG_FILENAME=app.log
    SHAREPOINT_HOST=your_sharepoint_host
    SHAREPOINT_SITE=your_sharepoint_site
    DRIVE_NAME=your_drive_name
    SEARCH_DATE=your_search_date
    USER_ACTIVITY_PERIOD=D7
    AUDIT_QUERY_DISPLAY_NAME=File Access Audit
    AUDIT_QUERY_START_DATE=2025-01-30T00:00:00
    AUDIT_QUERY_END_DATE=2025-01-31T00:00:00
    AUDIT_QUERY_RECORD_TYPE_FILTERS=sharePointFileOperation
    AUDIT_QUERY_MONITOR_INTERVAL=10
    AUDIT_QUERY_SUCCESS_STATUS=succeeded
    AUDIT_QUERY_RUNNING_STATUS=running
    AUDIT_QUERY_NOT_STARTED_STATUS=notStarted
    AUDIT_SHEET=Audit
    ```

## Usage

Run the `run.py` script to start collecting and exporting audit logs:
```sh
python run.py
```

## TODO

```python
    # TODO: Implement pagination in sharepoint_upload_activity, sharepoint_folder_activity, and sharepoint_subfolder_activity to retrieve all files, if applicable
    # TODO: Improve logging
```
