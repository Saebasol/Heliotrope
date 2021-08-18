from __future__ import annotations

from typing import Mapping, Optional, cast

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import NavigableString, Tag  # type: ignore


class HitomiBaseParser:
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
        return cast(list[Tag], galleryinfo.find_all("tr"))


class HitomiTagParser(HitomiBaseParser):
    def __init__(self, html: str, hitomi_type: str) -> None:
        super().__init__(html, hitomi_type)

    @property
    def title_element(self) -> Tag:
        title_element = self.gallery_element.find("h1")
        assert isinstance(title_element, Tag)
        title = title_element.find("a")
        assert isinstance(title, Tag)
        return title

    @property
    def thumbnail_element(self) -> Mapping[str, str]:
        picture_element = self.soup.find("picture")
        assert isinstance(picture_element, Tag)
        img_element = picture_element.find("img")
        assert isinstance(img_element, Tag)
        return cast(Mapping[str, str], img_element.attrs)

    @property
    def artist_element(self) -> list[Tag]:
        artist_element = self.soup.find("h2")
        assert isinstance(artist_element, Tag)
        return cast(list[Tag], artist_element.find_all("a"))

    @property
    def group_element(self) -> list[Tag]:
        return cast(list[Tag], self.infos[0].find_all("a"))

    @property
    def type_element(self) -> Tag:
        type_element = self.infos[1].find("a")
        assert isinstance(type_element, Tag)
        return type_element

    @property
    def language_element(self) -> Optional[Tag]:
        language_element = self.infos[2].find("a")
        assert not isinstance(language_element, NavigableString)
        return language_element

    @property
    def series_element(self) -> list[Tag]:
        return cast(list[Tag], self.infos[3].find_all("a"))

    @property
    def character_element(self) -> list[Tag]:
        return cast(list[Tag], self.infos[4].find_all("a"))

    @property
    def tags_element(self) -> list[Tag]:
        return cast(list[Tag], self.infos[5].find_all("a"))

    @property
    def date_element(self) -> Tag:
        date_elemment = self.soup.find("span", class_="date")
        assert isinstance(date_elemment, Tag)
        return date_elemment
