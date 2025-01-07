from heliotrope.core.exception import HeliotropeException


class GalleryinfoNotFound(HeliotropeException):
    def __init__(self) -> None:
        super().__init__("Galleryinfo not found.")
