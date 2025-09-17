from heliotrope.application.dtos.thumbnail import Size
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.resolved_image import ResolvedImage
from heliotrope.domain.repositories.resolved_image import ResolvedImageRepository


class GetResolvedImageUseCase:
    def __init__(self, resolved_image_repository: ResolvedImageRepository) -> None:
        self.resolved_image_repository = resolved_image_repository

    def execute(self, galleryinfo_id: int, file: File) -> ResolvedImage:
        return self.resolved_image_repository.resolve_image(galleryinfo_id, file)


class GetResolvedThumbnailUseCase:
    def __init__(self, resolved_image_repository: ResolvedImageRepository) -> None:
        self.resolved_image_repository = resolved_image_repository

    def execute(self, galleryinfo_id: int, file: File, size: Size) -> ResolvedImage:
        return self.resolved_image_repository.resolve_thumbnail(
            galleryinfo_id, file, size
        )
