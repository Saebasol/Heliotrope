"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from random import randrange
from typing import Optional, cast

from ameilisearch.client import Client

from heliotrope.abc import AbstractNoSQL
from heliotrope.domain.info import Info
from heliotrope.types import HitomiInfoJSON


class MeiliSearch(AbstractNoSQL):
    def __init__(
        self, url: str, api_key: Optional[str] = None, uid: str = "hitomi"
    ) -> None:
        self.client = Client(url, api_key)
        self.index = self.client.index(uid)

    def parse_query(self, querys: list[str]) -> tuple[str, list[str]]:
        parsed_query: list[str] = []
        title = ""
        for query in querys:
            if any(info_tag in query for info_tag in self.info_tags):
                splited = query.split(":")
                parsed_query.append(f"{splited[0]} = '{splited[1]}'")

            elif any(
                gender_common_tag in query
                for gender_common_tag in self.gender_common_tags
            ):
                parsed_query.append(f"tags = '{query}'")
            else:
                title = query

        return title, parsed_query

    async def add_infos(self, infos: list[Info]) -> None:
        async with self.index as index:
            await index.add_documents([dict(info.to_dict()) for info in infos])

    async def get_info(self, id: int) -> Info:
        async with self.index as index:
            d = cast(HitomiInfoJSON, await index.get_document(str(id)))
            return Info.from_dict(d)

    async def get_info_list(self, offset: int = 0, limit: int = 15) -> list[Info]:
        async with self.index as index:
            response = await index.search(
                "", {"sort": ["id:desc"], "offset": offset, "limit": limit}
            )
            return list(map(Info.from_dict, response["hits"]))

    async def get_random_info(self) -> Info:
        async with self.index as index:
            stats = await index.get_stats()
            total = stats["numberOfDocuments"]
            response = await index.get_documents(
                {"offset": randrange(total), "limit": 1}
            )
            d = cast(HitomiInfoJSON, response[0])
            return Info.from_dict(d)

    async def search(
        self,
        tags: list[str],
        offset: int = 0,
        limit: int = 15,
    ) -> list[Info]:
        title, tags = self.parse_query(tags)
        async with self.index as index:
            response = await index.search(
                title,
                {"sort": ["id:desc"], "filter": tags, "offset": offset, "limit": limit},
            )
            return list(map(Info.from_dict, response["hits"]))