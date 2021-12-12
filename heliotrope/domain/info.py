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

from bs4.element import Tag

from heliotrope.parser import Parser
from heliotrope.types import HitomiInfoJSON


def from_element(element: Tag) -> str:
    return element.text.strip().replace(" ", "_")


def from_elements(elements: list[Tag]) -> list[str]:
    return [from_element(element) for element in elements]


def tags_replacer(values: list[str]) -> list[str]:
    replaced: list[str] = []

    for value in values:
        if "♀" in value:
            removed_icon = value.replace("_♀", "")
            value = f"female:{removed_icon}"
        elif "♂" in value:
            removed_icon = value.replace("_♂", "")
            value = f"male:{removed_icon}"
        else:
            value = f"tag:{value}"

        replaced.append(value)

    return replaced


@dataclass
class Info:
    id: int
    title: str
    thumbnail: str
    artist: list[str]
    group: list[str]
    type: str
    language: str
    series: list[str]
    character: list[str]
    tags: list[str]
    date: str

    @classmethod
    def from_html(cls, id: int, html: str, hitomi_type: str) -> "Info":
        parser = Parser(html, hitomi_type)
        return cls(
            id=id,
            title=parser.title_element.text,
            thumbnail=parser.thumbnail_element.attrs["src"],
            artist=from_elements(parser.artist_elements),
            group=from_elements(parser.group_elements),
            type=from_element(parser.type_element),
            language=from_element(parser.language_element),
            series=from_elements(parser.series_elements),
            character=from_elements(parser.character_elements),
            tags=tags_replacer(from_elements(parser.tags_elements)),
            date=parser.date_element.text,
        )

    @classmethod
    def from_dict(cls, d: HitomiInfoJSON) -> "Info":
        return cls(
            id=int(d["id"]),
            title=d["title"],
            thumbnail=d["thumbnail"],
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
            id=str(self.id),
            title=self.title,
            thumbnail=self.thumbnail,
            artist=self.artist,
            group=self.group,
            type=self.type,
            language=self.language,
            series=self.series,
            character=self.character,
            tags=self.tags,
            date=self.date,
        )
