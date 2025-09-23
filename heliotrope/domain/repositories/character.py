from abc import ABC, abstractmethod


class CharacterRepository(ABC):
    @abstractmethod
    async def get_all_characters(self) -> list[str]:
        raise NotImplementedError
