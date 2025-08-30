from dataclasses import dataclass
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.language_localname import LanguageLocalname


@dataclass
class LanguageDTO(HeliotropeEntity):
    galleryid: Optional[int]
    language_localname: str
    name: str
    url: str

    @classmethod
    def from_domain(cls, language: Language):
        return cls(
            galleryid=language.galleryid,
            language_localname=language.language_localname.name,
            name=language.name,
            url=language.url,
        )

    def to_domain(self) -> Language:
        return Language(
            galleryid=self.galleryid,
            language_localname=LanguageLocalname(self.language_localname),
            name=self.name,
            url=self.url,
        )
