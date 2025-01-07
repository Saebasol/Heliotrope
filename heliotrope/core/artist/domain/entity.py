from dataclasses import dataclass

from heliotrope.core.base import HeliotropeEntity


@dataclass
class Artist(HeliotropeEntity):
    artist: str
    url: str
