# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from typing import Any, Optional, cast

from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore


class NoSQLQuery:
    def __init__(self, mongo_db_url: str) -> None:
        self.__client: Any = AsyncIOMotorClient(mongo_db_url)
        self.__collection = self.__client.hitomi.info

    def close(self) -> None:
        self.__client.close()

    async def get_info_list(
        self, offset: int = 0, limit: int = 15
    ) -> list[dict[str, Any]]:
        offset = offset * limit
        return cast(
            list[dict[str, Any]],
            await self.__collection.find({}, {"_id": 0})
            .sort("index", -1)
            .skip(offset)
            .limit(limit)
            .to_list(15),
        )

    async def search_info_list(
        self, query: list[str], offset: int = 0, limit: int = 15
    ) -> Optional[tuple[dict[str, Any], int]]:
        offset = offset * limit
        search_query: dict[str, Any] = {"$search": {"compound": {"must": []}}}
        for q in query:
            if ":" not in q:
                search_query["$search"]["compound"]["must"].append(
                    {"text": {"query": q.replace("_", " "), "path": "title"}}
                )
                continue
            tag_type, tag_name = q.split(":")
            tag_value = tag_name.replace("_", " ")
            if tag_type in [
                "group",
                "language",
                "series",
                "tags",
                "type",
                "artist",
                "characters",
                "female",
                "male",
                "tag",
            ]:
                gender_icon = {"female": " ♀", "male": " ♂"}
                query_value = f"{tag_value}{gender_icon.get(tag_type, '')}"
                tag_type = "tags" if tag_type in ["female", "male", "tag"] else tag_type
                search_query["$search"]["compound"]["must"].append(
                    {"text": {"query": query_value, "path": f"{tag_type}.value"}}
                )
        if count := (
            await self.__collection.aggregate(
                [search_query, {"$count": "count"}]
            ).to_list(1)
        ):
            result = await self.__collection.aggregate(
                [
                    search_query,
                    {"$skip": offset},
                    {"$limit": limit},
                    {"$project": {"_id": 0}},
                ]
            ).to_list(15)

            return result, count[0]["count"]

        return None

    async def find_info(self, index_id: int) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            await self.__collection.find_one({"index": index_id}, {"_id": 0}),
        )

    async def find_random_info(self) -> dict[str, Any]:
        info = await self.__collection.aggregate(
            [
                {"$sample": {"size": 1}},
                {"$project": {"_id": 0}},
            ]
        ).to_list(1)
        return cast(
            dict[str, Any],
            info[0],
        )

    async def insert_info(self, info: dict[str, Any]) -> None:
        return cast(None, await self.__collection.insert_one(info))
