from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class Group(HeliotropeEntity):
    group: str
    url: str
