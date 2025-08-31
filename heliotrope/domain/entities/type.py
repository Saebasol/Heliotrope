from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class Type(HeliotropeEntity):
    type: str
