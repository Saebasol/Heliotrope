from dataclasses import dataclass, field
from typing import Optional

from heliotrope.domain.file import File
from heliotrope.domain.tag import Tag
from heliotrope.types import HitomiGalleryinfoJSON


@dataclass
class Galleryinfo:
    id: str
    title: str
    japanese_title: Optional[str]
    language: str
    language_localname: str
    type: str
    date: str
    files: list[File] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)

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

    @classmethod
    def from_dict(cls, d: HitomiGalleryinfoJSON):
        return cls(
            id=d["id"],
            title=d["title"],
            japanese_title=d["japanese_title"],
            language=d["language"],
            language_localname=d["language_localname"],
            type=d["type"],
            date=d["date"],
            files=[File.from_dict(d["id"], file) for file in d["files"]],
            tags=[Tag.from_dict(d["id"], tag) for tag in d["tags"]],
        )
