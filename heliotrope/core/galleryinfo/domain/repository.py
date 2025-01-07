from abc import ABC, abstractmethod
from typing import Optional

from heliotrope.core.galleryinfo.domain.entity import Galleryinfo


class GalleryinfoRepository(ABC):
    @abstractmethod
    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_galleryinfo_ids(self, page: int = 1, item: int = 25) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_galleryinfo_ids(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_add_galleryinfo(self, galleryinfos: list[Galleryinfo]) -> None:
        raise NotImplementedError
