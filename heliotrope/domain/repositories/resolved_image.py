from abc import ABC, abstractmethod

from heliotrope.application.dtos.thumbnail import Size
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.resolved_image import ResolvedImage


class ResolvedImageRepository(ABC):
    @abstractmethod
    def resolve_image(self, galleryinfo_id: int, file: File) -> ResolvedImage:
        raise NotImplementedError

    @abstractmethod
    def resolve_thumbnail(
        self, galleryinfo_id: int, file: File, size: Size
    ) -> ResolvedImage:
        raise NotImplementedError
