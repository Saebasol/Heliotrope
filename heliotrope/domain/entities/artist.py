from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class Artist(HeliotropeEntity):
    artist: str
    url: str
