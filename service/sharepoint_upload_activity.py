import logging

import pandas as pd

from config import Config

from .base_sharepoint import BaseSharePointService

logger = logging.getLogger(__name__)


class SharePointUploadService(BaseSharePointService):
    async def search_files_by_creation_date(self, date, drive_id):
        headers = await self.get_headers("application/json")
        url = "https://graph.microsoft.com/v1.0/search/query"
        payload = {
            "requests": [
                {
                    "entityTypes": ["driveItem"],
                    "query": {
                        "queryString": f'created:{date} AND path:"{Config.SEARCH_QUERY_PATH}" AND ContentTypeId:0x0101*'
                    },
                    "fields": [
                        "name",
                        "webUrl",
                        "fileSystemInfo",
                        "createdBy",
                        "parentReference",
                    ],
                    "region": Config.SEARCH_QUERY_REGION,
                    "driveId": drive_id,
                }
            ]
        }
        response_data = await self.make_paginated_request_with_size(
            "POST", url, headers=headers, json=payload, size=Config.SEARCH_QUERY_SIZE
        )
        logger.debug("API Response: %s", response_data)
        return response_data

    @staticmethod
    def process_hits_response(data):
        if not data:
            logger.warning("No value found in the response.")
            return pd.DataFrame()

        structured_data = []
        for hit in data:
            resource = hit.get("resource", {})

            structured_data.append(
                {
                    "summary": hit.get("summary", ""),
                    "createdDateTime": resource.get("fileSystemInfo", {}).get(
                        "createdDateTime", ""
                    ),
                    "createdByEmail": resource.get("createdBy", {})
                    .get("user", {})
                    .get("email", ""),
                    "name": resource.get("name", ""),
                    "webUrl": resource.get("webUrl", ""),
                }
            )

        if not structured_data:
            logger.warning("No structured data found after processing hits.")
        else:
            logger.info("Processed %d hits successfully.", len(structured_data))

        return pd.DataFrame(structured_data)
