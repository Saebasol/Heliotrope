from dataclasses import dataclass
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.entities.language_localname import LanguageLocalname


@dataclass
class RawLanguage(HeliotropeEntity):
    galleryid: Optional[int]
    language_localname: str
    name: str
    url: str

    @classmethod
    def from_language(cls, language: Language) -> "RawLanguage":
        return cls(
            galleryid=language.galleryid,
            url=language.url,
            language_localname=language.language_localname.name,
            name=language.language_info.language,
        )

    def to_language(self) -> Language:
        return Language(
            galleryid=self.galleryid,
            url=self.url,
            language_localname=LanguageLocalname(self.language_localname),
            language_info=LanguageInfo(
                language=self.name,
                language_url=f"/index-{self.name.lower()}.html",
            ),
        )
