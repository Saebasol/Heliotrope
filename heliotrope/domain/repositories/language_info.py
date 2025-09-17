from abc import ABC, abstractmethod


class LanguageInfoRepository(ABC):
    @abstractmethod
    async def get_all_language_infos(self) -> list[str]:
        raise NotImplementedError
