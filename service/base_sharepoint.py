import logging

import aiohttp

from auth import TokenManager

logger = logging.getLogger(__name__)


class BaseSharePointService:
    def __init__(self):
        self.token_manager = TokenManager()

    async def get_access_token(self):
        return await self.token_manager.get_access_token()

    async def get_headers(self, content_type="application/json"):
        access_token = await self.get_access_token()
        return {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": content_type,
        }

    async def make_request(self, method, url, headers=None, json=None):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, headers=headers, json=json
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def make_paginated_request(
        self, method, url, headers=None, json=None, params=None
    ):
        results = []
        while url:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=json, params=params
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    results.extend(data.get("value", []))
                    url = data.get("@odata.nextLink")
                    params = None
        return results

    async def make_paginated_request_with_size(
        self, method, url, headers=None, json=None, size=100
    ):
        results = []
        from_index = 0
        while True:
            if json:
                json["requests"][0]["from"] = from_index
                json["requests"][0]["size"] = size
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=json
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    hits = data["value"][0].get("hitsContainers", [])[0].get("hits", [])
                    if not hits:
                        break
                    results.extend(hits)
                    from_index += size
        return results
