from heliotrope.domain.exceptions import HeliotropeException


class GalleryinfoNotFound(HeliotropeException):
    def __init__(self, message: str = "Galleryinfo not found.") -> None:
        super().__init__(message)
        self.message = message


class InfoNotFound(HeliotropeException):
    def __init__(self, message: str = "Info not found.") -> None:
        super().__init__(message)
        self.message = message
