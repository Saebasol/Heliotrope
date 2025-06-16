from heliotrope.domain.exceptions import GalleryinfoNotFound
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository


class DeleteGalleryinfoUseCase:
    def __init__(self, galleryinfo_repository: GalleryinfoRepository) -> None:
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, id: int) -> None:
        if not await self.galleryinfo_repository.is_galleryinfo_exists(id):
            raise GalleryinfoNotFound(str(int))
        await self.galleryinfo_repository.delete_galleryinfo(id)
