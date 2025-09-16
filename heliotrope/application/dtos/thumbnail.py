from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Size(Enum):
    SMALLSMALL = "smallsmall"
    SMALL = "small"
    SMALLBIG = "smallbig"
    BIG = "big"


@dataclass
class GetThumbnailQueryDTO:
    size: Size
    single: Literal["true", "false"]
