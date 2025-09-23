from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class AllTags(HeliotropeEntity):
    artists: list[str]
    characters: list[str]
    groups: list[str]
    language: list[str]
    series: list[str]
    tag: list[str]
    female: list[str]
    male: list[str]
    type: list[str]
