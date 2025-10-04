from dataclasses import dataclass

from heliotrope.domain.entities.info import Info
from heliotrope.domain.serializer import Serializer


@dataclass
class PostSearchQueryDTO:
    offset: int


@dataclass
class PostSearchBodyDTO:
    query: list[str]


@dataclass
class SearchResultDTO(Serializer):
    results: list[Info]
    count: int
