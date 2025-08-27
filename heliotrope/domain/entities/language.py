from dataclasses import dataclass
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.language_localname import LanguageLocalname


@dataclass
class Language(HeliotropeEntity):
    galleryid: Optional[int]
    language_localname: LanguageLocalname
    name: str
    url: str
