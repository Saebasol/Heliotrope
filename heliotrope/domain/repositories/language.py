from abc import ABC, abstractmethod

from heliotrope.domain.entities.language import Language


class LanguageRepository(ABC):
    @abstractmethod
    async def create_language(self, language: Language) -> Language:
        raise NotImplementedError
