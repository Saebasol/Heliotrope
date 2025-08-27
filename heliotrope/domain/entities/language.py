from dataclasses import dataclass
from typing import Optional

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.language_localname import LangaugeLocalname


@dataclass
class Language(HeliotropeEntity):
    galleryid: Optional[int]
    language_localname: LangaugeLocalname
    name: str
    url: str
