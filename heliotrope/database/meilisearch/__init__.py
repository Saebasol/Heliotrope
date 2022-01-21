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
from ameilisearch.errors import MeiliSearchApiError
from ameilisearch.index import Index
from sanic.log import logger

from heliotrope.abc.database import AbstractInfoDatabase
from heliotrope.domain.info import Info
from heliotrope.types import HitomiInfoJSON
from heliotrope.utils import is_the_first_process


class MeiliSearch(AbstractInfoDatabase):
    def __init__(self, client: Client, index: Index) -> None:
        self.client = client
        self.index = index
        self.total = 0

    async def close(self) -> None:
        logger.debug(f"close {self.__class__.__name__}")
        await self.client.close()
        await self.index.close()

    @classmethod
    async def setup(
        cls, url: str, api_key: Optional[str] = None, uid: str = "hitomi"
    ) -> "MeiliSearch":
        logger.debug(f"Setting up {cls.__name__}")
        async with Client(url, api_key) as client:
            task = await client.create_index(uid)
            await client.wait_for_task(task["uid"])
            async with await client.get_index(uid) as index:
                if is_the_first_process:
                    await index.update_filterable_attributes(
                        [
                            "tags",
                            "artist",
                            "group",
                            "type",
                            "language",
                            "series",
                            "character",
                        ]
                    )
                    await index.update_sortable_attributes(["id"])
                    await index.update_searchable_attributes(["title"])
                instance = cls(client, index)
                stats = await index.get_stats()
                instance.total = stats["numberOfDocuments"]
                return instance

    def parse_query(self, querys: list[str]) -> tuple[str, list[str]]:
        # Tags are received in the following format: female:big_breasts
        # If it is not in the following format, it is regarded as a title.
        # 태그는 다음과 같은 형식으로 받아요: female:big_breasts
        # 만약 다음과 같은 형식이 아니라면 제목으로 간주해요.
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

    async def get_all_index(self) -> list[int]:
        results = await self.index.get_documents({"limit": self.total})
        return list(map(lambda d: d["index"], results))

    async def add_infos(self, infos: list[Info]) -> None:
        await self.index.add_documents([dict(info.to_dict()) for info in infos])

    async def get_info(self, id: int) -> Optional[Info]:
        try:
            d = cast(HitomiInfoJSON, await self.index.get_document(str(id)))
        except MeiliSearchApiError:
            return None
        return Info.from_dict(d)

    async def get_info_list(self, offset: int = 0, limit: int = 15) -> list[Info]:
        response = await self.index.search(
            "", {"sort": ["id:desc"], "offset": offset, "limit": limit}
        )
        return list(map(Info.from_dict, response["hits"]))

    async def get_random_info(self) -> Info:
        response = await self.index.get_documents(
            {"offset": randrange(self.total), "limit": 1}
        )
        d = cast(HitomiInfoJSON, response[0])
        return Info.from_dict(d)

    async def search(
        self,
        tags: list[str],
        offset: int = 0,
        limit: int = 15,
    ) -> tuple[list[Info], int]:
        title, tags = self.parse_query(tags)
        response = await self.index.search(
            title,
            {"sort": ["id:desc"], "filter": tags, "offset": offset, "limit": limit},
        )
        return list(map(Info.from_dict, response["hits"])), response["nbHits"]
