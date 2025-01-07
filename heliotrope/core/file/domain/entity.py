from dataclasses import dataclass, field
from heliotrope.core.base import HeliotropeEntity


@dataclass
class File(HeliotropeEntity):
    def __post_init__(self):
        self.hasavif = bool(self.hasavif)
        self.hasjxl = bool(self.hasjxl)
        self.haswebp = bool(self.haswebp)
        self.single = bool(self.single)

    hasavif: bool
    hash: str
    height: int
    name: str
    width: int
    hasjxl: bool = field(default=False)
    haswebp: bool = field(default=False)
    single: bool = field(default=False)
