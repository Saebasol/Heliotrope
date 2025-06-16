class HeliotropeException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GalleryinfoNotFound(HeliotropeException):
    def __init__(
        self,
        message: str = "Galleryinfo not found.",
    ) -> None:
        super().__init__(message)

    @classmethod
    def from_id(cls, id: int) -> "GalleryinfoNotFound":
        return cls(f"Galleryinfo with ID {id} not found.")


class InfoNotFound(HeliotropeException):
    def __init__(
        self,
        message: str = "Info not found.",
    ) -> None:
        super().__init__(message)

    @classmethod
    def from_id(cls, id: int) -> "InfoNotFound":
        return cls(f"Info with ID {id} not found.")

    @classmethod
    def from_query(cls, query: list[str]) -> "InfoNotFound":
        query_str = ", ".join(query)
        return cls(f"Info not found for query: {query_str}")
