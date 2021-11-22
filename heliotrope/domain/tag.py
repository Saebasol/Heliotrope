from dataclasses import dataclass
from typing import Literal, Optional

from heliotrope.types import HitomiTagJSON


@dataclass
class Tag:
    index_id: str
    male: Optional[Literal["", "1"]]
    female: Optional[Literal["", "1"]]
    tag: str
    url: str
    id: Optional[int] = None

    def to_dict(self) -> HitomiTagJSON:
        hitomi_tag_json = HitomiTagJSON(url=self.url, tag=self.tag)

        if self.male is not None:
            hitomi_tag_json["male"] = self.male

        if self.female is not None:
            hitomi_tag_json["female"] = self.female

        return hitomi_tag_json

    @classmethod
    def from_dict(cls, index_id: str, d: HitomiTagJSON):
        return cls(
            index_id=index_id,
            male=d.get("male"),
            female=d.get("female"),
            tag=d["tag"],
            url=d["url"],
        )
