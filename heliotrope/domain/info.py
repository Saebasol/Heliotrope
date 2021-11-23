from dataclasses import dataclass
from typing import Optional


@dataclass
class ValueUrl:
    value: str
    url: str


@dataclass
class Info:
    title: str
    thumbnail: str
    artist: list[ValueUrl]
    group: list[ValueUrl]
    type: Optional[ValueUrl]
    language: Optional[ValueUrl]
    series: list[ValueUrl]
    character: list[ValueUrl]
    tags: list[ValueUrl]
    date: str
