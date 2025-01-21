from dataclasses import dataclass, field
from heliotrope.core.base import HeliotropeEntity


@dataclass
class File(HeliotropeEntity):
    hasavif: bool
    hash: str
    height: int
    name: str
    width: int
    hasjxl: bool = field(default=False)
    haswebp: bool = field(default=False)
    single: bool = field(default=False)
