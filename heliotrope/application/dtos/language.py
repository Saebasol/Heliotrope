from dataclasses import dataclass
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.entities.language_localname import LanguageLocalname


@dataclass
class LanguageDTO(HeliotropeEntity):
    galleryid: Optional[int]
    language_localname: str
    name: str
    url: str

    @classmethod
    def from_domain(cls, language: Language) -> "LanguageDTO":
        return cls(
            galleryid=language.galleryid,
            language_localname=language.language_localname.name,
            name=language.language_info.language,
            url=language.language_info.language_url,
        )

    def to_domain(self) -> Language:
        return Language(
            galleryid=self.galleryid,
            language_localname=LanguageLocalname(self.language_localname),
            language_info=LanguageInfo(
                language=self.name,
                language_url=self.url,
            ),
        )
