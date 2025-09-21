from abc import ABC, abstractmethod

from heliotrope.domain.entities.language_info import LanguageInfo


class LanguageInfoRepository(ABC):
    @abstractmethod
    async def get_or_add_language_info(self, language_info: LanguageInfo) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_language_infos(self) -> list[str]:
        raise NotImplementedError
