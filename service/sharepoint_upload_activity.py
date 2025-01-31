import aiohttp
import pandas as pd
from auth import TokenManager
from config import Config
import logging

logger = logging.getLogger(__name__)

async def search_files_by_creation_date(date, drive_id):
    access_token = await TokenManager().get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    url = "https://graph.microsoft.com/v1.0/search/query"
    payload = {
        "requests": [
            {
                "entityTypes": ["driveItem"],
                "query": {
                    "queryString": f"created:{date} AND path:\"{Config.SEARCH_QUERY_PATH}\" AND ContentTypeId:0x0101*"
                },
                "fields": ["name", "webUrl", "fileSystemInfo", "createdBy", "parentReference"],
                "region": Config.SEARCH_QUERY_REGION,
                "driveId": drive_id,
                "size": Config.SEARCH_QUERY_SIZE
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            response_data = await response.json()
            logger.debug("🔍 API Response: %s", response_data)  # Log the response data
            return response_data

def process_hits_response(data):
    if not isinstance(data, dict) or 'value' not in data or not data['value']:
        logger.warning("⚠️ No value found in the response.")
        return pd.DataFrame()

    hits_containers = data['value'][0].get('hitsContainers', [])
    if not hits_containers:
        logger.warning("⚠️ No hitsContainers found in the response.")
        return pd.DataFrame()

    hits = hits_containers[0].get('hits', [])
    if not hits:
        logger.warning("⚠️ No hits found in the hitsContainers.")
        return pd.DataFrame()

    structured_data = []
    for hit in hits:
        resource = hit.get('resource', {})

        structured_data.append({
            'summary': hit.get('summary', ''),
            'createdDateTime': resource.get('fileSystemInfo', {}).get('createdDateTime', ''),
            'createdByEmail': resource.get('createdBy', {}).get('user', {}).get('email', ''),
            'name': resource.get('name', ''),
            'webUrl': resource.get('webUrl', '')
        })

    if not structured_data:
        logger.warning("⚠️ No structured data found after processing hits.")
    else:
        logger.info("✅ Processed %d hits successfully.", len(structured_data))

    return pd.DataFrame(structured_data)