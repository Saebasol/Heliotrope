from dataclasses import dataclass

from heliotrope.domain.base import HeliotropeEntity
from heliotrope.domain.entities.file import File


@dataclass
class ResolvedImage(HeliotropeEntity):
    url: str
    file: File
