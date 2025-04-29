from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class Parody(HeliotropeEntity):
    parody: str
    url: str
