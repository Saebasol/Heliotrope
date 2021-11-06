from typing import Optional

from heliotrope.domain.file import HitomiFile
from heliotrope.domain.tag import HitomiTag
from heliotrope.shared.domain_model import DomainModel
from heliotrope.types import HitomiFileJSON, HitomiGalleryinfoJSON, HitomiTagJSON


class HitomiGalleryInfo(DomainModel):
    def __init__(
        self,
        title: str,
        date: str,
        type: str,
        japanese_title: Optional[str],
        language: str,
        files: list[HitomiFileJSON],
        id: str,
        language_localname: str,
        tags: list[HitomiTagJSON],
    ) -> None:
        self.title = title
        self.date = date
        self.type = type
        self.japanese_title = japanese_title
        self.language = language
        self.files: list[HitomiFile] = [HitomiFile.from_dict(file) for file in files]
        self.id = id
        self.language_localname = language_localname
        self.tags: list[HitomiTag] = [HitomiTag.from_dict(tag) for tag in tags]

    @classmethod
    def from_dict(cls, d: HitomiGalleryinfoJSON) -> "HitomiGalleryInfo":
        return cls(
            title=d["title"],
            date=d["date"],
            type=d["type"],
            japanese_title=d["japanese_title"],
            language=d["language"],
            files=d["files"],
            id=d["id"],
            language_localname=d["language_localname"],
            tags=d["tags"],
        )

    def to_dict(self) -> HitomiGalleryinfoJSON:
        return HitomiGalleryinfoJSON(
            title=self.title,
            date=self.date,
            type=self.type,
            japanese_title=self.japanese_title,
            language=self.language,
            files=[file.to_dict() for file in self.files],
            id=self.id,
            language_localname=self.language_localname,
            tags=[tag.to_dict() for tag in self.tags],
        )

    def __eq__(self, other: DomainModel) -> bool:
        return self.to_dict() == other.to_dict()
