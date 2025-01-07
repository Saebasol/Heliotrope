from dataclasses import dataclass, field
from heliotrope.core.base import HeliotropeEntity


@dataclass
class Tag(HeliotropeEntity):

    def __post_init__(self):
        if self.female in ["0", 0, None, ""]:
            self.female = False

        if self.female in ["1", 1]:
            self.female = True

        if self.male in ["0", 0, None, ""]:
            self.male = False

        if self.male in ["1", 1]:
            self.male = True

    tag: str
    url: str
    female: bool = field(default=False)
    male: bool = field(default=False)
