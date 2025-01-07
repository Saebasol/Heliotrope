from heliotrope.core.galleryinfo.domain.entity import Galleryinfo
from heliotrope.core.galleryinfo.domain.repository import GalleryinfoRepository


class AddGalleryinfoUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, galleryinfo: Galleryinfo) -> None:
        await self.galleryinfo_repository.add_galleryinfo(galleryinfo)


class BulkAddGalleryinfoUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, galleryinfos: list[Galleryinfo]) -> None:
        await self.galleryinfo_repository.bulk_add_galleryinfo(galleryinfos)
