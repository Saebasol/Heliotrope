from abc import ABC, abstractmethod

from heliotrope.domain.entities.type import Type


class TypeRepository(ABC):
    @abstractmethod
    async def get_or_add_type(self, type: Type) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_types(self) -> list[str]:
        raise NotImplementedError
