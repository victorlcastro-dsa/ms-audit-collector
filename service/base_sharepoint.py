import aiohttp
from auth import TokenManager
import logging

logger = logging.getLogger(__name__)


class BaseSharePointService:
    def __init__(self):
        self.token_manager = TokenManager()

    async def get_access_token(self):
        return await self.token_manager.get_access_token()

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
