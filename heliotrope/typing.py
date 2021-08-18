from typing import Literal, Optional, TypedDict


class HitomiFilesJSON(TypedDict):
    width: int
    hash: str
    haswebp: int
    name: str
    height: int


class HitomiTagsJSON(TypedDict):
    male: Optional[Literal["", "1"]]
    female: Optional[Literal["", "1"]]
    url: str
    tag: str


class HitomiGalleryinfoJSON(TypedDict):
    language_localname: str
    language: str
    date: str
    files: list[HitomiFilesJSON]
    tags: list[HitomiTagsJSON]
    japanese_title: Optional[str]
    title: str
    id: str
    type: str
