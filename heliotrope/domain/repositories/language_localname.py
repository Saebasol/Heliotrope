from abc import ABC, abstractmethod

from heliotrope.domain.entities.language_localname import LanguageLocalname


class LanguageLocalnameRepository(ABC):
    @abstractmethod
    async def get_or_create_localname(
        self, localname: LanguageLocalname
    ) -> LanguageLocalname:
        raise NotImplementedError
