from abc import ABC, abstractmethod

from heliotrope.domain.entities.language import Language


class LanguageRepository(ABC):
    @abstractmethod
    async def get_all_languages(self) -> list[Language]:
        raise NotImplementedError
