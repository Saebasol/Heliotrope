from dataclasses import dataclass

from heliotrope.domain.entities.info import Info
from heliotrope.domain.serializer import Serializer


@dataclass
class ListResultDTO(Serializer):
    list: list[Info]
    count: int
