from typing import TypeVar, Literal, Optional, TypedDict


T = TypeVar("T")


class _HitomiFileJSONOptional(TypedDict, total=False):
    hasavifsmalltn: Literal[1]
    hasavif: Literal[1]


class HitomiFileJSON(_HitomiFileJSONOptional):
    width: int
    hash: str
    haswebp: Literal[0, 1]
    name: str
    height: int


class _HitomiTagJSONOptional(TypedDict, total=False):
    male: Optional[Literal["", "1"]]
    female: Optional[Literal["", "1"]]


class HitomiTagJSON(_HitomiTagJSONOptional):
    url: str
    tag: str


class HitomiGalleryinfoJSON(TypedDict):
    date: str
    title: str
    type: str
    japanese_title: Optional[str]
    language: str
    files: list[HitomiFileJSON]
    id: str
    language_localname: str
    tags: list[HitomiTagJSON]
