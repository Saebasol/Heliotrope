from dataclasses import dataclass, field
from typing import Literal, Optional

from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String
from heliotrope.types import HitomiFileJSON, HitomiGalleryinfoJSON, HitomiTagJSON

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Galleryinfo:
    __table__ = Table(
        "galleryinfo",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("index_id", String, nullable=False),
        Column("title", String, nullable=False),
        Column("japanese_title", String),
        Column("language", String, nullable=False),
        Column("language_localname", String, nullable=False),
        Column("type", String, nullable=False),
        Column("date", String, nullable=False),
    )

    index_id: str
    title: str
    japanese_title: Optional[str]
    language: str
    language_localname: str
    type: str
    date: str
    files: list["File"] = field(default_factory=list)
    tags: list["Tag"] = field(default_factory=list)
    id: Optional[int] = None

    __mapper_args__ = {  # type: ignore
        "properties": {"files": relationship("File"), "tags": relationship("Tag")}
    }

    def to_dict(self) -> HitomiGalleryinfoJSON:
        return HitomiGalleryinfoJSON(
            title=self.title,
            date=self.date,
            type=self.type,
            japanese_title=self.japanese_title,
            language=self.language,
            files=[file.to_dict() for file in self.files],
            id=self.index_id,
            language_localname=self.language_localname,
            tags=[tag.to_dict() for tag in self.tags],
        )

    @classmethod
    def from_dict(cls, d: HitomiGalleryinfoJSON):
        return cls(
            index_id=d["id"],
            title=d["title"],
            japanese_title=d["japanese_title"],
            language=d["language"],
            language_localname=d["language_localname"],
            type=d["type"],
            date=d["date"],
            files=[File.from_dict(d["id"], file) for file in d["files"]],
            tags=[Tag.from_dict(d["id"], tag) for tag in d["tags"]],
        )


@mapper_registry.mapped
@dataclass
class File:
    __table__ = Table(
        "file",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("index_id", String, ForeignKey("galleryinfo.index_id")),
        Column("name", String, nullable=False),
        Column("width", Integer, nullable=False),
        Column("height", Integer, nullable=False),
        Column("hash", String(64), nullable=False),
        Column("haswebp", Integer, nullable=False),
        Column("hasavifsmalltn", Integer),
        Column("hasavif", Integer),
    )

    index_id: str
    name: str
    width: int
    height: int
    hash: str
    haswebp: Literal[0, 1]
    hasavifsmalltn: Optional[Literal[1]] = None
    hasavif: Optional[Literal[1]] = None
    id: Optional[int] = None

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

    @classmethod
    def from_dict(cls, index_id: str, d: HitomiFileJSON):
        return cls(
            index_id=index_id,
            name=d["name"],
            width=d["width"],
            height=d["height"],
            hash=d["hash"],
            haswebp=d["haswebp"],
            hasavifsmalltn=d.get("hasavifsmalltn"),
            hasavif=d.get("hasavif"),
        )


@mapper_registry.mapped
@dataclass
class Tag:
    __table__ = Table(
        "tag",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("index_id", String, ForeignKey("galleryinfo.index_id")),
        Column("male", String(1)),
        Column("female", String(1)),
        Column("tag", String, nullable=False),
        Column("url", String, nullable=False),
    )

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
