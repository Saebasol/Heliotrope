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

from heliotrope.domain.file import File
from heliotrope.domain.tag import Tag
from heliotrope.types import HitomiGalleryinfoJSON


@dataclass
class Galleryinfo:
    id: int
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
            id=str(self.id),
            language_localname=self.language_localname,
            tags=[tag.to_dict() for tag in self.tags],
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
            files=[File.from_dict(int_id, file) for file in d["files"]],
            tags=[Tag.from_dict(int_id, tag) for tag in d["tags"]],
        )
