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
from typing import Optional
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


class BaseParser:
    HITOMI_TYPE_MAPPING = {
        "manga": "manga",
        "doujinshi": "dj",
        "cg": "acg",
        "gamecg": "cg",
        "anime": "anime",
    }

    def __init__(self, html: str, hitomi_type: str) -> None:
        self.__html = html
        self.__hitomi_type = hitomi_type

    @property
    def soup_type(self) -> str:
        return self.HITOMI_TYPE_MAPPING[self.__hitomi_type]

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.__html, "lxml")

    @property
    def gallery_element(self) -> Tag:
        gallery_element = self.soup.find(
            "div", {"class": f"gallery {self.soup_type}-gallery"}
        )
        assert isinstance(gallery_element, Tag)
        return gallery_element

    @property
    def infos(self) -> list[Tag]:
        galleryinfo = self.gallery_element.find("div", {"class": "gallery-info"})
        assert isinstance(galleryinfo, Tag)
        return galleryinfo.find_all("tr")


class Parser:
    def __init__(self, html: str, hitomi_type: str) -> None:
        self.base_parser = BaseParser(html, hitomi_type)

    @property
    def title_element(self) -> Tag:
        title_element = self.base_parser.gallery_element.find("h1")
        assert isinstance(title_element, Tag)
        title = title_element.find("a")
        assert isinstance(title, Tag)
        return title

    @property
    def thumbnail_element(self) -> Tag:
        picture_element = self.base_parser.soup.find("picture")
        assert isinstance(picture_element, Tag)
        img_element = picture_element.find("img")
        assert isinstance(img_element, Tag)
        return img_element

    @property
    def artist_elements(self) -> list[Tag]:
        artist_element = self.base_parser.soup.find("h2")
        assert isinstance(artist_element, Tag)
        return artist_element.find_all("a")

    @property
    def group_elements(self) -> list[Tag]:
        return self.base_parser.infos[0].find_all("a")

    @property
    def type_element(self) -> Tag:
        type_element = self.base_parser.infos[1].find("a")
        assert isinstance(type_element, Tag)
        return type_element

    @property
    def language_element(self) -> Optional[Tag]:
        language_element = self.base_parser.infos[2].find("a")
        assert not isinstance(language_element, NavigableString)
        return language_element

    @property
    def series_elements(self) -> list[Tag]:
        return self.base_parser.infos[3].find_all("a")

    @property
    def character_elements(self) -> list[Tag]:
        return self.base_parser.infos[4].find_all("a")

    @property
    def tags_elements(self) -> list[Tag]:
        return self.base_parser.infos[5].find_all("a")

    @property
    def date_element(self) -> Tag:
        date_elemment = self.base_parser.soup.find("span", class_="date")
        assert isinstance(date_elemment, Tag)
        return date_elemment
