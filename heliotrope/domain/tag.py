from typing import Literal, Optional

from heliotrope.shared.domain_model import DomainModel
from heliotrope.types import HitomiTagJSON


class HitomiTag(DomainModel):
    def __init__(
        self,
        url: str,
        tag: str,
        male: Optional[Literal["", "1"]] = None,
        female: Optional[Literal["", "1"]] = None,
    ) -> None:
        self.url = url
        self.tag = tag
        self.male: Optional[Literal["", "1"]] = male
        self.female: Optional[Literal["", "1"]] = female

    @classmethod
    def from_dict(cls, d: HitomiTagJSON) -> "HitomiTag":
        return cls(
            url=d["url"], tag=d["tag"], male=d.get("male"), female=d.get("female")
        )

    def to_dict(self) -> HitomiTagJSON:
        hitomi_tag_json = HitomiTagJSON(url=self.url, tag=self.tag)

        if self.male is not None:
            hitomi_tag_json["male"] = self.male

        if self.female is not None:
            hitomi_tag_json["female"] = self.female

        return hitomi_tag_json
