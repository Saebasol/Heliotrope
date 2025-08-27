from abc import ABC, abstractmethod

from heliotrope.domain.entities.tag import Tag


class TagRepository(ABC):
    @abstractmethod
    async def get_all_tags(self) -> list[Tag]:
        raise NotImplementedError
