from typing import Optional, Self, TypedDict

from pymongo import AsyncMongoClient


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


class MongoDB:
    def __init__(
        self, client: AsyncMongoClient[HitomiInfoJSON], is_atlas: bool
    ) -> None:
        self.client = client
        self.collection = self.client.hitomi.info
        self.is_atlas = is_atlas

    @classmethod
    async def create(cls, mongodb_url: str) -> Self:
        client: AsyncMongoClient[HitomiInfoJSON] = AsyncMongoClient(mongodb_url)
        return cls(client, "mongodb.net" in mongodb_url)
