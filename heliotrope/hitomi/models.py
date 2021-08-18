from __future__ import annotations

from typing import Any, Iterator, Literal, Optional

from bs4.element import Tag  # type: ignore

from heliotrope.hitomi.parser import HitomiTagParser
from heliotrope.typing import HitomiFilesJSON, HitomiGalleryinfoJSON, HitomiTagsJSON


class HitomiFiles:
    """
    Make hitomi files object from json response
    """

    def __init__(self, response: HitomiFilesJSON) -> None:
        self.__response = response

    @property
    def width(self) -> int:
        return self.__response["width"]

    @property
    def hash(self) -> str:
        return self.__response["hash"]

    @property
    def haswebp(self) -> int:
        return self.__response["haswebp"]

    @property
    def name(self) -> str:
        return self.__response["name"]

    @property
    def height(self) -> int:
        return self.__response["height"]

    @classmethod
    def to_generator(cls, files: list[HitomiFilesJSON]) -> Iterator["HitomiFiles"]:
        for file in files:
            yield cls(file)

    def to_dict(self) -> HitomiFilesJSON:
        return {
            "width": self.width,
            "hash": self.hash,
            "haswebp": self.haswebp,
            "name": self.name,
            "height": self.height,
        }


class HitomiTags:
    """
    Make hitomi tags object from json response
    """

    def __init__(self, response: HitomiTagsJSON) -> None:
        self.__response = response

    @property
    def male(self) -> Optional[Literal["", "1"]]:
        return self.__response.get("male")

    @property
    def female(self) -> Optional[Literal["", "1"]]:
        return self.__response.get("female")

    @property
    def url(self) -> str:
        return self.__response["url"]

    @property
    def tag(self) -> str:
        return self.__response["tag"]

    @classmethod
    def to_generator(cls, tags: list[HitomiTagsJSON]) -> Iterator["HitomiTags"]:
        for tag in tags:
            yield HitomiTags(tag)

    @classmethod
    def parse_tags(cls, tag: HitomiTagsJSON) -> dict[str, str]:
        return {
            "value": f"{'female' if tag['female'] else 'male' if tag['male'] else 'tag'}: {tag['tag']}",
            "url": tag["url"],
        }

    def to_parse_dict(self) -> dict[str, str]:
        return self.parse_tags(self.to_dict())

    def to_dict(self) -> HitomiTagsJSON:
        return {
            "male": self.male,
            "female": self.female,
            "url": self.url,
            "tag": self.tag,
        }


class HitomiGalleryinfo:
    """
    Make hitomi galleryinfo object from json response
    """

    def __init__(self, response: HitomiGalleryinfoJSON) -> None:
        self.__response = response

    @property
    def language_localname(self) -> str:
        return self.__response["language_localname"]

    @property
    def language(self) -> str:
        return self.__response["language"]

    @property
    def date(self) -> str:
        return self.__response["date"]

    @property
    def files(self) -> Iterator[HitomiFiles]:
        return HitomiFiles.to_generator(self.__response["files"])

    @property
    def tags(self) -> Iterator[HitomiTags]:
        return HitomiTags.to_generator(self.__response["tags"])

    @property
    def japanese_title(self) -> Optional[str]:
        return self.__response.get("japanese_title")

    @property
    def title(self) -> str:
        return self.__response["title"]

    @property
    def id(self) -> str:
        return self.__response["id"]

    @property
    def type(self) -> str:
        return self.__response["type"]

    def to_dict(self) -> HitomiGalleryinfoJSON:
        return {
            "language_localname": self.language_localname,
            "language": self.language,
            "date": self.date,
            "files": [file.to_dict() for file in self.files],
            "tags": [tag.to_dict() for tag in self.tags],
            "japanese_title": self.japanese_title,
            "title": self.title,
            "id": self.id,
            "type": self.type,
        }


# NOTE: value, url 객체로 나누는것도 한번 생각해볼만함
class HitomiInfo:
    def __init__(self, html: str, hitomi_type: str) -> None:
        # 상속해서 쓰니까 지저분했음
        self.__parser = HitomiTagParser(html, hitomi_type)

    def __parse_list_element(self, elements: list[Tag]) -> list[dict[str, str]]:
        return [
            {"value": element.text, "url": str(element.attrs["href"])}
            for element in elements
        ]

    def __parse_single_element(
        self, elements: Optional[Tag]
    ) -> Optional[dict[str, str]]:
        if not elements:
            return None
        return {
            "value": elements.text.replace(" ", "").replace("\n", ""),
            "url": str(elements.attrs["href"]),
        }

    @property
    def title(self) -> str:
        return str(self.__parser.title_element.text)

    @property
    def thumbnail(self) -> str:
        return self.__parser.thumbnail_element["src"]

    @property
    def artist(self) -> list[dict[str, str]]:
        return self.__parse_list_element(self.__parser.artist_element)

    @property
    def group(self) -> list[dict[str, str]]:
        return self.__parse_list_element(self.__parser.group_element)

    @property
    def type(self) -> Optional[dict[str, str]]:
        return self.__parse_single_element(self.__parser.type_element)

    @property
    def language(self) -> Optional[dict[str, str]]:
        return self.__parse_single_element(self.__parser.language_element)

    @property
    def series(self) -> list[dict[str, str]]:
        return self.__parse_list_element(self.__parser.series_element)

    @property
    def character(self) -> list[dict[str, str]]:
        return self.__parse_list_element(self.__parser.character_element)

    @property
    def tags(self) -> list[dict[str, str]]:
        return self.__parse_list_element(self.__parser.tags_element)

    @property
    def date(self) -> str:
        return str(self.__parser.date_element.text)

    def to_dict(self) -> Any:
        return {
            "title": self.title,
            "thumbnail": self.thumbnail,
            "artist": self.artist,
            "group": self.group,
            "type": self.type,
            "language": self.language,
            "series": self.series,
            "character": self.character,
            "tags": self.tags,
            "date": self.date,
        }
