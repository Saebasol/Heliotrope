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

    async def get_list(self, offset: int = 0, limit: int = 15) -> list[Info]:
        async with self.index as index:
            response = await index.search(
                "", {"sort": ["id:asc"], "offset": offset, "limit": limit}
            )
            return list(map(Info.from_dict, response["hits"]))

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
                {"sort": ["id:asc"], "filter": tags, "offset": offset, "limit": limit},
            )
            return list(map(Info.from_dict, response["hits"]))
