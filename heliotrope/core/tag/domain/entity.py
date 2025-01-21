from dataclasses import dataclass, field
from heliotrope.core.base import HeliotropeEntity


@dataclass
class Tag(HeliotropeEntity):
    tag: str
    url: str
    female: bool = field(default=False)
    male: bool = field(default=False)
