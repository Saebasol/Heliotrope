from abc import ABC, abstractmethod
from typing import Optional

from heliotrope.domain.entities.info import Info


class InfoRepository(ABC):
    @abstractmethod
    async def get_info(self, id: int) -> Optional[Info]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_info_ids(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def add_info(self, info: Info) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_list_info(self, page: int = 1, item: int = 25) -> list[Info]:
        raise NotImplementedError

    @abstractmethod
    async def search_by_query(
        self, query: list[str], page: int = 0, item: int = 25
    ) -> tuple[int, list[Info]]:
        raise NotImplementedError

    @abstractmethod
    async def get_random_info(self, query: list[str]) -> Info | None:
        raise NotImplementedError
