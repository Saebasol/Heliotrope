from dataclasses import dataclass
from heliotrope.core.base import HeliotropeEntity


@dataclass
class Character(HeliotropeEntity):
    character: str
    url: str
