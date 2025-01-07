from dataclasses import dataclass
from heliotrope.core.base import HeliotropeEntity


@dataclass
class Group(HeliotropeEntity):
    group: str
    url: str
