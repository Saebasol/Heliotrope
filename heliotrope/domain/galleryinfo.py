"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from dataclasses import dataclass, field
from typing import Optional

from heliotrope.domain.artist import Artist
from heliotrope.domain.character import Character
from heliotrope.domain.file import File
from heliotrope.domain.group import Group
from heliotrope.domain.language import Language
from heliotrope.domain.parody import Parody
from heliotrope.domain.related import Related
from heliotrope.domain.tag import Tag
from heliotrope.domain.scene_index import SceneIndex
from heliotrope.types import HitomiGalleryinfoJSON


@dataclass
class Galleryinfo:
    id: int
    type: str
    date: str
    # title
    title: str
    japanese_title: Optional[str] = None
    # video
    video: Optional[str] = None
    videofilename: Optional[str] = None
    # language
    language_url: Optional[str] = None
    language_localname: Optional[str] = None
    language: Optional[str] = None
    languages: list[Language] = field(default_factory=list)
    # tags
    files: list[File] = field(default_factory=list)
    tags: Optional[list[Tag]] = None
    artists: Optional[list[Artist]] = None
    characters: Optional[list[Character]] = None
    groups: Optional[list[Group]] = None
    parodys: Optional[list[Parody]] = None
    scene_indexes: list[SceneIndex] = field(default_factory=list)
    related: list[Related] = field(default_factory=list)

    def to_dict(self) -> HitomiGalleryinfoJSON:
        return HitomiGalleryinfoJSON(
            id=self.id,
            type=self.type,
            date=self.date,
            title=self.title,
            japanese_title=self.japanese_title,
            video=self.video,
            videofilename=self.videofilename,
            language_url=self.language_url,
            language_localname=self.language_localname,
            language=self.language,
            languages=[language.to_dict() for language in self.languages],
            files=[file.to_dict() for file in self.files],
            related=[related.to_id() for related in self.related],
            scene_indexes=[
                scene_index.to_index() for scene_index in self.scene_indexes
            ],
            tags=[tag.to_dict() for tag in self.tags] if self.tags else None,
            artists=[artist.to_dict() for artist in self.artists]
            if self.artists
            else None,
            characters=[character.to_dict() for character in self.characters]
            if self.characters
            else None,
            groups=[group.to_dict() for group in self.groups] if self.groups else None,
            parodys=[parody.to_dict() for parody in self.parodys]
            if self.parodys
            else None,
        )

    @classmethod
    def from_dict(cls, d: HitomiGalleryinfoJSON) -> "Galleryinfo":
        int_id = int(d["id"])
        return cls(
            id=int_id,
            title=d["title"],
            japanese_title=d["japanese_title"],
            language=d["language"],
            language_localname=d["language_localname"],
            type=d["type"],
            date=d["date"],
            languages=[
                Language.from_dict(int_id, language) for language in d["languages"]
            ],
            related=[Related.from_dict(int_id, related) for related in d["related"]],
            files=[File.from_dict(int_id, file) for file in d["files"]],
            scene_indexes=[
                SceneIndex.from_dict(int_id, scene_index)
                for scene_index in d["scene_indexes"]
            ],
            tags=[Tag.from_dict(int_id, tag) for tag in d["tags"]] if d["tags"] else [],
            artists=[Artist.from_dict(int_id, artist) for artist in d["artists"]]
            if d["artists"]
            else [],
            characters=[
                Character.from_dict(int_id, character) for character in d["characters"]
            ]
            if d["characters"]
            else [],
            groups=[Group.from_dict(int_id, group) for group in d["groups"]]
            if d["groups"]
            else [],
            parodys=[Parody.from_dict(int_id, parody) for parody in d["parodys"]]
            if d["parodys"]
            else [],
        )
