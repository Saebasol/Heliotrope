from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional, Self, get_type_hints

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.tag import Tag


def parse_tags_dict_list(tags_dict_list: list[Any]) -> list[str]:
    return [
        str(v).replace(" ", "_")
        for tags in tags_dict_list
        for k, v in tags.items()
        if k != "url"
        if k != "galleryurl"
        if k != "language_url"
    ]


def parse_male_female_tag(tag: Tag) -> str:
    tag_name = tag.tag.replace(" ", "_")
    if tag.female:
        return f"female:{tag_name}"
    if tag.male:
        return f"male:{tag_name}"
    return f"tag:{tag_name}"


@dataclass
class Info(HeliotropeEntity):
    id: int
    title: str
    thumbnail: File
    artists: list[str]
    groups: list[str]
    type: str
    language: Optional[str]
    series: list[str]
    characters: list[str]
    tags: list[str]
    date: datetime

    @classmethod
    def from_galleryinfo(cls, galleryinfo: Galleryinfo) -> Self:
        galleryinfo_dict = asdict(galleryinfo)
        info_dict: dict[str, Any] = {}
        type_hints = get_type_hints(cls)

        for key, value in type_hints.items():
            if key in galleryinfo_dict:
                if value == list[str]:
                    if key == "tags":
                        info_dict[key] = [
                            parse_male_female_tag(Tag.from_dict(tag))
                            for tag in galleryinfo_dict[key]
                        ]
                    else:
                        info_dict[key] = parse_tags_dict_list(galleryinfo_dict[key])
                else:
                    info_dict[key] = galleryinfo_dict[key]

        if "series" in type_hints and "parodys" in galleryinfo_dict:
            info_dict["series"] = parse_tags_dict_list(galleryinfo_dict["parodys"])
        info_dict["thumbnail"] = File.from_dict(galleryinfo_dict["files"][0])
        info_dict["language"] = galleryinfo_dict["language_localname"]["name"]
        return cls(**info_dict)
