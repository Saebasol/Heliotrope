from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from dataclasses import dataclass
from dataclasses import field

from heliotrope.core.artist.domain.entity import Artist
from heliotrope.core.character.domain.entity import Character
from heliotrope.core.file.domain.entity import File
from heliotrope.core.group.domain.entity import Group
from heliotrope.core.language.domain.entity import Language
from heliotrope.core.parody.domain.entity import Parody
from heliotrope.core.tag.domain.entity import Tag
from heliotrope.core.base import HeliotropeEntity


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
    artists: list[Artist] = field(default_factory=list)
    characters: list[Character] = field(default_factory=list)
    files: list[File] = field(default_factory=list)
    groups: list[Group] = field(default_factory=list)
    languages: list[Language] = field(default_factory=list)
    parodys: list[Parody] = field(default_factory=list)
    related: list[int] = field(default_factory=list)
    scene_indexes: list[int] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)
