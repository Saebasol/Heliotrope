class HeliotropeException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GalleryinfoNotFound(HeliotropeException):
    def __init__(self, message: str = "Galleryinfo not found.") -> None:
        super().__init__(message)
        self.message = message


class InfoNotFound(HeliotropeException):
    def __init__(self, message: str = "Info not found.") -> None:
        super().__init__(message)
        self.message = message
