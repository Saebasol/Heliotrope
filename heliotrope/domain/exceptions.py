class HeliotropeException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GalleryinfoNotFound(HeliotropeException):
    def __init__(
        self,
        additional_info: str,
        message: str = "Galleryinfo not found.",
    ) -> None:
        message = f"{message} {additional_info}"
        super().__init__(message)


class InfoNotFound(HeliotropeException):
    def __init__(
        self,
        additional_info: str,
        message: str = "Info not found.",
    ) -> None:
        message = f"{message} {additional_info}"
        super().__init__(message)
