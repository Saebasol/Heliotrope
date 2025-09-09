from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.entities.character import Character
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.group import Group
from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.entities.language_localname import LanguageLocalname
from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.entities.raw_language import RawLanguage
from heliotrope.domain.entities.tag import Tag
from heliotrope.domain.entities.type import Type


@dataclass
class RawGalleryinfo(HeliotropeEntity):
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
    languages: list[RawLanguage] = field(default_factory=list[RawLanguage])
    parodys: list[Parody] = field(default_factory=list[Parody])
    related: list[int] = field(default_factory=list[int])
    scene_indexes: list[int] = field(default_factory=list[int])
    tags: list[Tag] = field(default_factory=list[Tag])

    @classmethod
    def from_galleryinfo(cls, galleryinfo: Galleryinfo) -> RawGalleryinfo:
        return cls(
            date=galleryinfo.date,
            galleryurl=galleryinfo.galleryurl,
            id=galleryinfo.id,
            japanese_title=galleryinfo.japanese_title,
            language_localname=galleryinfo.language_localname.name,
            language_url=galleryinfo.language_info.language_url,
            language=galleryinfo.language_info.language,
            title=galleryinfo.title,
            type=galleryinfo.type.type,
            video=galleryinfo.video,
            videofilename=galleryinfo.videofilename,
            blocked=galleryinfo.blocked,
            datepublished=galleryinfo.datepublished,
            artists=galleryinfo.artists,
            characters=galleryinfo.characters,
            files=galleryinfo.files,
            groups=galleryinfo.groups,
            languages=[
                RawLanguage.from_language(lang) for lang in galleryinfo.languages
            ],
            parodys=galleryinfo.parodys,
            related=galleryinfo.related,
            scene_indexes=galleryinfo.scene_indexes,
            tags=galleryinfo.tags,
        )

    def to_galleryinfo(self) -> Galleryinfo:
        return Galleryinfo(
            date=self.date,
            galleryurl=self.galleryurl,
            id=self.id,
            japanese_title=self.japanese_title,
            language_localname=LanguageLocalname(self.language_localname),
            language_info=LanguageInfo(
                language=self.language,
                language_url=self.language_url,
            ),
            title=self.title,
            type=Type(self.type),
            video=self.video,
            videofilename=self.videofilename,
            blocked=self.blocked,
            datepublished=self.datepublished,
            artists=self.artists,
            characters=self.characters,
            files=self.files,
            groups=self.groups,
            languages=[lang.to_language() for lang in self.languages],
            parodys=self.parodys,
            related=self.related,
            scene_indexes=self.scene_indexes,
            tags=self.tags,
        )
