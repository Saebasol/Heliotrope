# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

# Motor 라이브러리는 유형 주석이 적용 되어있지 않기때문에 여러 타입 관련 문제를 무시합니다.
# The Motor library ignores many type-related issues because type annotations are not applied.

from typing import Any, Optional, cast

from motor.core import AgnosticClient, AgnosticCollection  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from heliotrope.abc.database import AbstractInfoDatabase
from heliotrope.domain.info import Info
from heliotrope.types import HitomiInfoJSON


class ODM(AbstractInfoDatabase):
    def __init__(
        self, client: Any, is_atlas: bool = False, use_atlas_search: bool = False
    ) -> None:
        self.client: AgnosticClient = client
        self.collection: AgnosticCollection = self.client.hitomi.info
        self.is_atlas = is_atlas
        self.use_atlas_search = use_atlas_search

    def close(self) -> None:
        self.client.close()

    @classmethod
    def setup(cls, mongo_db_url: str, use_atlas_search: bool = False) -> "ODM":
        is_atlas = "mongodb.net" in mongo_db_url
        return cls(AsyncIOMotorClient(mongo_db_url), is_atlas, use_atlas_search)

    async def get_all_index(self) -> list[int]:
        ids: list[int] = []
        id: int
        async for id in self.collection.find({}, {"id": 1}):
            ids.append(id)
        return ids

    async def add_info(self, info: Info) -> None:
        await self.collection.insert_one(info.to_dict())

    async def get_info(self, id: int) -> Optional[Info]:
        info_json = cast(
            Optional[HitomiInfoJSON],
            await self.collection.find_one({"id": id}, {"_id": 0}),
        )
        if info_json:
            return Info.from_dict(info_json)

        return None

    async def get_info_list(self, offset: int = 0, limit: int = 15) -> list[Info]:
        offset = offset * limit

        info_jsons = cast(
            list[HitomiInfoJSON],
            await self.collection.find({}, {"_id": 0})
            .sort("id", -1)
            .skip(offset)
            .limit(limit)
            .to_list(15),
        )
        return [Info.from_dict(json_info) for json_info in info_jsons]

    async def get_random_info(self) -> Info:
        info_json = cast(
            HitomiInfoJSON,
            await self.collection.aggregate(
                [
                    {"$sample": {"size": 1}},
                    {"$project": {"_id": 0}},
                ]
            ).next(),
        )

        return Info.from_dict(info_json)

    def parse_query(self, querys: list[str]) -> tuple[str, dict[str, Any]]:
        # Tags are received in the following format: female:big_breasts
        # If it is not in the following format, it is regarded as a title.
        # 태그는 다음과 같은 형식으로 받습니다.: female:big_breasts
        # 만약 다음과 같은 형식이 아니라면 제목으로 간주합니다.
        query_dict: dict[str, Any] = {}
        title = ""
        for query in querys:
            if any(info_tag in query for info_tag in self.info_tags):
                splited = query.split(":")
                query_dict.update({splited[0]: splited[1]})
            elif any(
                gender_common_tag in query
                for gender_common_tag in self.gender_common_tags
            ):
                query_dict.update({"tags": query})
            else:
                title = query

        return title, query_dict

    def make_pipeline(
        self, title: str, query: dict[str, Any], offset: int = 0, limit: int = 15
    ) -> list[dict[str, Any]]:
        pipeline: list[dict[str, Any]] = [
            {"$match": query},
            {
                "$group": {
                    "_id": 0,
                    "count": {"$sum": 1},
                    "list": {"$push": "$$ROOT"},
                }
            },
            {"$skip": offset},
            {"$limit": limit},
            {"$project": {"_id": 0, "list": {"_id": 0}}},
        ]
        if title:
            if self.is_atlas and self.use_atlas_search:
                pipeline.insert(
                    0,
                    {
                        "$search": {
                            "compound": {
                                "must": [{"text": {"query": title, "path": "title"}}]
                            }
                        }
                    },
                )
            else:
                pipeline[0]["$match"].update({"$text": {"$search": title}})

        return pipeline

    async def search(
        self, querys: list[str], offset: int = 0, limit: int = 15
    ) -> tuple[list[Info], int]:

        offset = offset * limit
        title, query = self.parse_query(querys)
        pipeline = self.make_pipeline(title, query, offset, limit)

        try:
            results: dict[str, Any] = await self.collection.aggregate(pipeline).next()
        except StopAsyncIteration:
            results = {"list": [], "count": 0}

        return [
            Info.from_dict(cast(HitomiInfoJSON, result)) for result in results["list"]
        ], results["count"]