from abc import ABC, abstractmethod
from typing import Optional

from heliotrope.domain.entities.galleryinfo import Galleryinfo


class GalleryinfoRepository(ABC):
    @abstractmethod
    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_galleryinfo_ids(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> int:
        raise NotImplementedError
