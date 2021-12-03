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
from heliotrope.parser import Parser
from bs4.element import Tag
from heliotrope.types import HitomiInfoValueUrlJSON, HitomiInfoJSON


@dataclass
class ValueUrl:
    value: str
    url: str

    def to_dict(self) -> HitomiInfoValueUrlJSON:
        return HitomiInfoValueUrlJSON(value=self.value, url=self.url)

    @classmethod
    def from_element(cls, element: Tag) -> "ValueUrl":
        return cls(value=element.text.strip(), url=element.attrs["href"])

    @classmethod
    def from_elements_with_tags_replacer(cls, elements: list[Tag]):
        replaced: list[ValueUrl] = []

        for element in elements:
            value = element.text.strip()

            if value in " ♀":
                removed_icon = value.replace(" ♀", "")
                value = f"female:{removed_icon}"
            elif value in " ♂":
                removed_icon = value.replace(" ♂", "")
                value = f"male:{removed_icon}"
            else:
                value = f"tag:{value}"

            replaced.append(cls(value=value, url=element.attrs["href"]))

        return replaced

    @classmethod
    def from_elements(cls, elements: list[Tag]) -> list["ValueUrl"]:
        return [cls.from_element(element) for element in elements]


@dataclass
class Info:
    title: str
    thumbnail: str
    artist: list[ValueUrl]
    group: list[ValueUrl]
    type: ValueUrl
    language: ValueUrl
    series: list[ValueUrl]
    character: list[ValueUrl]
    tags: list[ValueUrl]
    date: str

    @classmethod
    def from_html(cls, html: str, hitomi_type: str) -> "Info":
        parser = Parser(html, hitomi_type)
        return cls(
            title=parser.title_element.text,
            thumbnail=parser.thumbnail_element.attrs["src"],
            artist=ValueUrl.from_elements(parser.artist_elements),
            group=ValueUrl.from_elements(parser.group_elements),
            type=ValueUrl.from_element(parser.type_element),
            language=ValueUrl.from_element(parser.language_element),
            series=ValueUrl.from_elements(parser.series_elements),
            character=ValueUrl.from_elements(parser.character_elements),
            tags=ValueUrl.from_elements_with_tags_replacer(parser.tags_elements),
            date=parser.date_element.text,
        )

    def to_dict(self) -> HitomiInfoJSON:
        return HitomiInfoJSON(
            title=self.title,
            thumbnail=self.thumbnail,
            artist=[artist.to_dict() for artist in self.artist],
            group=[group.to_dict() for group in self.group],
            type=self.type.to_dict(),
            language=self.language.to_dict(),
            series=[series.to_dict() for series in self.series],
            character=[character.to_dict() for character in self.character],
            tags=[tags.to_dict() for tags in self.tags],
            date=self.date,
        )
