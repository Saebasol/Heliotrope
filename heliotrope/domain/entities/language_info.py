from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class LanguageInfo(HeliotropeEntity):
    language: str
    language_url: str
