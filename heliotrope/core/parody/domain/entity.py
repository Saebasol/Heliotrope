from dataclasses import dataclass
from heliotrope.core.base import HeliotropeEntity


@dataclass
class Parody(HeliotropeEntity):
    parody: str
    url: str
