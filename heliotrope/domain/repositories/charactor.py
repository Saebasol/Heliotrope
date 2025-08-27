from abc import ABC, abstractmethod

from heliotrope.domain.entities.character import Character


class CharacterRepository(ABC):
    @abstractmethod
    async def get_all_characters(self) -> list[Character]:
        raise NotImplementedError
