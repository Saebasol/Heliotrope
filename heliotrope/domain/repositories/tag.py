from abc import ABC, abstractmethod

from heliotrope.domain.entities.tag import Tag


class TagRepository(ABC):
    @abstractmethod
    async def get_or_add_tag(self, tag: Tag) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_tags(self) -> list[tuple[str, bool, bool]]:
        raise NotImplementedError
