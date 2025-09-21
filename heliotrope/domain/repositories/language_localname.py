from abc import ABC, abstractmethod

from heliotrope.domain.entities.language_localname import LanguageLocalname


class LanguageLocalnameRepository(ABC):
    @abstractmethod
    async def get_or_add_localname(self, localname: LanguageLocalname) -> int:
        raise NotImplementedError
