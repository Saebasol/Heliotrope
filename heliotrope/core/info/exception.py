from heliotrope.core.exception import HeliotropeException


class InfoNotFound(HeliotropeException):
    def __init__(self) -> None:
        super().__init__("Info not found.")
