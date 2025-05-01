from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.entities.character import Character
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.group import Group
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.entities.tag import Tag


@dataclass
class Galleryinfo(HeliotropeEntity):
    date: datetime
    galleryurl: str
    id: int
    japanese_title: Optional[str]
    language_localname: str
    language_url: str
    language: str
    title: str
    type: str
    video: Optional[str]
    videofilename: Optional[str]
    blocked: bool = field(default=False)
    datepublished: Optional[date] = field(default=None)
    artists: list[Artist] = field(default_factory=list[Artist])
    characters: list[Character] = field(default_factory=list[Character])
    files: list[File] = field(default_factory=list[File])
    groups: list[Group] = field(default_factory=list[Group])
    languages: list[Language] = field(default_factory=list[Language])
    parodys: list[Parody] = field(default_factory=list[Parody])
    related: list[int] = field(default_factory=list[int])
    scene_indexes: list[int] = field(default_factory=list[int])
    tags: list[Tag] = field(default_factory=list[Tag])
