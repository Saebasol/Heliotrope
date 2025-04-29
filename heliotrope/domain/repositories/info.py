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
    async def bulk_add_info(self, infos: list[Info]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_list_info(self, page: int = 1, item: int = 25) -> list[Info]:
        raise NotImplementedError
