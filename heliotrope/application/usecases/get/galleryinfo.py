from typing import Generator

from heliotrope.application.exceptions import GalleryinfoNotFound
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository


class GetGalleryinfoUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, id: int) -> Galleryinfo:
        galleryinfo = await self.galleryinfo_repository.get_galleryinfo(id)

        if galleryinfo is None:
            raise GalleryinfoNotFound

        return galleryinfo


class GetGalleryinfoIdsUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, page: int = 1, item: int = 25) -> list[int]:
        return await self.galleryinfo_repository.get_galleryinfo_ids(page, item)


class GetAllGalleryinfoIdsUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    def __await__(self) -> Generator[None, None, list[int]]:
        return self.execute().__await__()

    async def execute(self) -> list[int]:
        return await self.galleryinfo_repository.get_all_galleryinfo_ids()
