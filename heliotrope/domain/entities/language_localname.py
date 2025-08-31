from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity


@dataclass
class LanguageLocalname(HeliotropeEntity):
    name: str
