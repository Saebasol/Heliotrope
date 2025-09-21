from abc import ABC, abstractmethod

from heliotrope.domain.entities.character import Character


class CharacterRepository(ABC):
    @abstractmethod
    async def get_or_create_character(self, character: Character) -> Character:
        raise NotImplementedError

    @abstractmethod
    async def get_all_characters(self) -> list[str]:
        raise NotImplementedError
