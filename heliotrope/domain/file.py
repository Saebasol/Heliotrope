from typing import Literal, Optional

from heliotrope.shared.domain_model import DomainModel
from heliotrope.types import HitomiFileJSON


class HitomiFile(DomainModel):
    def __init__(
        self,
        width: int,
        hash: str,
        haswebp: Literal[0, 1],
        name: str,
        height: int,
        hasavif: Optional[Literal[1]] = None,
        hasavifsmalltn: Optional[Literal[1]] = None,
    ) -> None:
        self.width = width
        self.hash = hash
        self.haswebp: Literal[0, 1] = haswebp
        self.name = name
        self.height = height
        self.hasavif: Optional[Literal[1]] = hasavif
        self.hasavifsmalltn: Optional[Literal[1]] = hasavifsmalltn

    @classmethod
    def from_dict(cls, d: HitomiFileJSON) -> "HitomiFile":
        return cls(
            width=d["width"],
            hash=d["hash"],
            haswebp=d["haswebp"],
            name=d["name"],
            height=d["height"],
            hasavif=d.get("hasavif"),
            hasavifsmalltn=d.get("hasavifsmalltn"),
        )

    def to_dict(self) -> HitomiFileJSON:
        hitomi_file_json = HitomiFileJSON(
            width=self.width,
            hash=self.hash,
            haswebp=self.haswebp,
            name=self.name,
            height=self.height,
        )
        if self.hasavif is not None:
            hitomi_file_json["hasavif"] = self.hasavif

        if self.hasavifsmalltn is not None:
            hitomi_file_json["hasavifsmalltn"] = self.hasavifsmalltn

        return hitomi_file_json

    def __eq__(self, other: DomainModel) -> bool:
        return self.to_dict() == other.to_dict()
