from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.entities.character import Character
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.group import Group
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.entities.tag import Tag


@dataclass
class GalleryinfoDTO:
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

    @classmethod
    def from_domain(cls, galleryinfo: Galleryinfo):
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
            languages=galleryinfo.languages,
            parodys=galleryinfo.parodys,
            related=galleryinfo.related,
            scene_indexes=galleryinfo.scene_indexes,
            tags=galleryinfo.tags,
        )

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "galleryurl": self.galleryurl,
            "id": self.id,
            "japanese_title": self.japanese_title,
            "language_localname": self.language_localname,
            "language_url": self.language_url,
            "language": self.language,
            "title": self.title,
            "type": self.type,
            "video": self.video,
            "videofilename": self.videofilename,
            "blocked": self.blocked,
            "datepublished": self.datepublished,
            "artists": [artist.to_dict() for artist in self.artists],
            "characters": [character.to_dict() for character in self.characters],
            "files": [file.to_dict() for file in self.files],
            "groups": [group.to_dict() for group in self.groups],
            "languages": [language.to_dict() for language in self.languages],
            "parodys": [parody.to_dict() for parody in self.parodys],
            "related": self.related,
            "scene_indexes": self.scene_indexes,
            "tags": [tag.to_dict() for tag in self.tags],
        }
