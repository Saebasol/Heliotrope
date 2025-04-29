from typing import Optional, TypedDict

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

    async def get_info(self, id: int) -> Optional[Info]:
        info_json = await self.mongodb.collection.find_one({"id": id}, {"_id": 0})

        if info_json:
            return Info.from_dict(info_json)

        return None

    async def get_all_info_ids(self) -> list[int]:
        ids = await self.mongodb.collection.find({}, {"id": 1, "_id": 0}).to_list()
        return [id["id"] for id in ids]

    async def add_info(self, info: Info) -> None:
        await self.mongodb.collection.insert_one(HitomiInfoJSON(**info.to_dict()))

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
