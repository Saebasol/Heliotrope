from dataclasses import dataclass


@dataclass
class PostSearchQueryDTO:
    offset: int


@dataclass
class PostSearchBodyDTO:
    query: list[str]
