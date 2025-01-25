from typing import Optional, Self, TypedDict
from pymongo import AsyncMongoClient, uri_parser


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
        self, client: AsyncMongoClient[HitomiInfoJSON], use_atlas_search: bool
    ) -> None:
        self.client = client
        self.collection = self.client.hitomi.info
        self.use_atlas_search = use_atlas_search

    @classmethod
    async def create(cls, mongodb_url: str, use_atlas_search: bool = False) -> Self:
        return cls(AsyncMongoClient(mongodb_url), use_atlas_search)
