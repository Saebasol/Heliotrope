from abc import ABC, abstractmethod

from heliotrope.domain.entities.language_info import LanguageInfo


class LanguageInfoRepository(ABC):
    @abstractmethod
    async def get_all_language_infos(self) -> list[LanguageInfo]:
        raise NotImplementedError
