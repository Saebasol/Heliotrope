from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository


class CreateGalleryinfoUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, galleryinfo: Galleryinfo) -> None:
        await self.galleryinfo_repository.add_galleryinfo(galleryinfo)


class BulkCreateGalleryinfoUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, galleryinfos: list[Galleryinfo]) -> None:
        await self.galleryinfo_repository.bulk_add_galleryinfo(galleryinfos)
