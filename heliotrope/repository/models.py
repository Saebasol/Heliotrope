from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Galleryinfo:
    __table__ = Table(
        "galleryinfo",
        mapper_registry.metadata,
        Column("id", String, primary_key=True),
        Column("title", String, nullable=False),
        Column("japanese_title ", String),
        Column("language", String, nullable=False),
        Column("language_localname", String, nullable=False),
        Column("type", String, nullable=False),
        Column("date", String, nullable=False),
    )

    id: str
    title: str
    japanese_title: Optional[str]
    language: str
    language_localname: str
    type: str
    date: str
    files: list["File"] = field(default_factory=list)
    tags: list["Tag"] = field(default_factory=list)

    __mapper_args__ = {  # type: ignore
        "properties": {"files": relationship("File"), "tags": relationship("Tag")}
    }


@mapper_registry.mapped
@dataclass
class File:
    __table__ = Table(
        "file",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("galleryinfo_id", String, ForeignKey("galleryinfo.id")),
        Column("name", String, nullable=False),
        Column("width", Integer, nullable=False),
        Column("height", Integer, nullable=False),
        Column("hash", String(64), nullable=False),
        Column("haswebp", Integer, nullable=False),
        Column("hasavifsmalltn", Integer),
        Column("hasavif", Integer),
    )

    id: int
    galleryinfo_id: Optional[str]
    name: str
    width: int
    height: int
    hash: str
    haswebp: int
    hasavifsmalltn: Optional[int]
    hasavif: Optional[int]


@mapper_registry.mapped
@dataclass
class Tag:
    __table__ = Table(
        "tag",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("galleryinfo_id", String, ForeignKey("galleryinfo.id")),
        Column("male", String(1)),
        Column("female", String(1)),
        Column("tag", String, nullable=False),
        Column("url", String, nullable=False),
    )

    id: int
    galleryinfo_id: str
    male: Optional[str]
    female: Optional[str]
    tag: str
    url: str
