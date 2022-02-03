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
from dataclasses import dataclass
from typing import Mapping, Optional

from heliotrope.domain.file import File
from heliotrope.domain.galleryinfo import Galleryinfo
from heliotrope.domain.tag import Tag
from heliotrope.types import HitomiInfoJSON


def parse_tags_dict_list(tags_dict_list: list[Mapping[str, object]]) -> list[str]:
    return [str(v) for tags in tags_dict_list for k, v in tags.items() if k != "url"]


def parse_male_female_tag(tag: Tag) -> str:
    tag_name = tag.tag.replace(" ", "_")
    if tag.male:
        return f"male:{tag_name}"
    if tag.female:
        return f"female:{tag_name}"
    return f"tag:{tag_name}"


@dataclass
class Info:
    id: int
    title: str
    thumbnail: File
    artist: list[str]
    group: list[str]
    type: str
    language: Optional[str]
    series: list[str]
    character: list[str]
    tags: list[str]
    date: str

    @classmethod
    def from_galleryinfo(cls, galleryinfo: Galleryinfo) -> "Info":
        return cls(
            id=galleryinfo.id,
            title=galleryinfo.title,
            thumbnail=galleryinfo.files[0],
            artist=parse_tags_dict_list(
                [artist.to_dict() for artist in galleryinfo.artists]
            )
            if galleryinfo.artists
            else [],
            group=parse_tags_dict_list(
                [group.to_dict() for group in galleryinfo.groups]
            )
            if galleryinfo.groups
            else [],
            type=galleryinfo.type,
            language=galleryinfo.language,
            series=parse_tags_dict_list(
                [parody.to_dict() for parody in galleryinfo.parodys]
            )
            if galleryinfo.parodys
            else [],
            character=parse_tags_dict_list(
                [character.to_dict() for character in galleryinfo.characters]
            )
            if galleryinfo.characters
            else [],
            tags=[parse_male_female_tag(tag) for tag in galleryinfo.tags]
            if galleryinfo.tags
            else [],
            date=galleryinfo.date,
        )

    @classmethod
    def from_dict(cls, d: HitomiInfoJSON) -> "Info":
        return cls(
            id=int(d["id"]),
            title=d["title"],
            thumbnail=File.from_dict(int(d["id"]), d["thumbnail"]),
            artist=d["artist"],
            group=d["group"],
            type=d["type"],
            language=d["language"],
            series=d["series"],
            character=d["character"],
            tags=d["tags"],
            date=d["date"],
        )

    def to_dict(self) -> HitomiInfoJSON:
        return HitomiInfoJSON(
            id=self.id,
            title=self.title,
            thumbnail=self.thumbnail.to_dict(),
            artist=self.artist,
            group=self.group,
            type=self.type,
            language=self.language,
            series=self.series,
            character=self.character,
            tags=self.tags,
            date=self.date,
        )
