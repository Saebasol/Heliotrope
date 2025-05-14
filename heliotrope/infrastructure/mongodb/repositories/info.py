from typing import Any, Optional, TypedDict, cast

from heliotrope.domain.entities.info import Info
from heliotrope.domain.repositories.info import InfoRepository
from heliotrope.infrastructure.mongodb import MongoDB


class HitomiFileJSON(TypedDict):
    width: int
    hash: str
    haswebp: bool
    hasavif: bool
    name: str
    height: int


class HitomiInfoJSON(TypedDict):
    id: int
    title: str
    thumbnail: HitomiFileJSON
    artist: list[str]
    group: list[str]
    type: str
    language: Optional[str]
    series: list[str]
    character: list[str]
    tags: list[str]
    date: str


class MongoDBInfoRepository(InfoRepository):
    def __init__(
        self,
        mongodb: MongoDB,
        use_atlas_search: bool = False,
    ) -> None:
        self.mongodb = mongodb
        self.use_atlas_search = use_atlas_search and self.mongodb.is_atlas

    async def get_info(self, id: int) -> Optional[Info]:
        info_json = await self.mongodb.collection.find_one({"id": id}, {"_id": 0})

        if info_json:
            return Info.from_dict(info_json)

        return None

    async def get_all_info_ids(self) -> list[int]:
        ids = await self.mongodb.collection.find({}, {"id": 1, "_id": 0}).to_list()
        return [id["id"] for id in ids]

    async def add_info(self, info: Info) -> int:
        await self.mongodb.collection.insert_one(HitomiInfoJSON(**info.to_dict()))
        return info.id

    async def bulk_add_info(self, infos: list[Info]) -> None:
        await self.mongodb.collection.insert_many(
            [HitomiInfoJSON(**info.to_dict()) for info in infos]
        )

    async def get_list_info(self, page: int = 1, item: int = 25) -> list[Info]:
        offset = page * item
        infos: list[Info] = []

        async for json_info in await self.mongodb.collection.aggregate(
            [
                {"$project": {"_id": 0}},
                {"$sort": {"id": -1}},
                {"$skip": offset},
                {"$limit": item},
            ],
            allowDiskUse=True,
        ):
            infos.append(Info.from_dict(json_info))
        return infos

    def _parse_query(self, query: list[str]) -> tuple[str, dict[str, Any]]:
        # Tags are received in the following format: female:big_breasts
        # If it is not in the following format, it is regarded as a title.
        info_tags = ["artist", "group", "type", "language", "series", "character"]
        gender_common_tags = ["female", "tags", "male"]
        query_dict: dict[str, Any] = {}

        title = ""
        for data in query:
            if data.startswith(tuple(info_tags)):
                tag = data.split(":")
                key = tag[0]
                value = tag[1]
                if key in query_dict:
                    query_dict[key]["$all"].append(value)
                else:
                    query_dict[key] = {"$all": [value]}
            elif data.startswith(tuple(gender_common_tags)):
                if "tags" in query_dict:
                    query_dict["tags"]["$all"].append(data)
                else:
                    query_dict["tags"] = {"$all": [data]}
            else:
                title = data
        return title, query_dict

    def make_pipeline(
        self, query: list[str], offset: int, item: int
    ) -> list[dict[str, Any]]:
        title, query_dict = self._parse_query(query)

        pipeline: list[dict[str, Any]] = [
            {"$project": {"_id": 0}},
            {"$match": query_dict},
            {"$sort": {"id": -1}},
        ]
        if self.use_atlas_search:
            pipeline.insert(
                0,
                {
                    "$search": {
                        "index": "default",
                        "text": {
                            "query": title,
                            "path": ["title"],
                        },
                    }
                },
            )
        else:
            pipeline[1]["$match"]["title"] = {"$regex": title, "$options": "i"}

        return pipeline

    async def search_by_query(
        self, query: list[str], page: int = 0, item: int = 25
    ) -> tuple[int, list[Info]]:
        offset = page * item

        pipeline = self.make_pipeline(query, offset, item)
        pipeline.extend(
            [
                {"$skip": offset},
                {"$limit": item},
            ]
        )

        count_cursor = await self.mongodb.collection.aggregate(
            [
                pipeline[0] if self.use_atlas_search else pipeline[1],
                {"$count": "count"},
            ],
            allowDiskUse=True,
        )
        result_cursor = await self.mongodb.collection.aggregate(
            pipeline, allowDiskUse=True
        )

        count_list = await count_cursor.to_list()
        if not count_list:
            return 0, []

        count_dict = cast(dict[str, Any], count_list[0])

        return count_dict["count"], [
            Info.from_dict(info) async for info in result_cursor
        ]

    async def get_random_info(self, query: list[str]) -> Info | None:
        pipeline = self.make_pipeline(query, 0, 1)
        pipeline.append({"$sample": {"size": 1}})

        async for json_info in await self.mongodb.collection.aggregate(
            pipeline, allowDiskUse=True
        ):
            return Info.from_dict(json_info)
