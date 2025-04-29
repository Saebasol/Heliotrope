from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class Character(HeliotropeEntity):
    character: str
    url: str
