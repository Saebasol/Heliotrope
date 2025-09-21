from abc import ABC, abstractmethod

from heliotrope.domain.entities.type import Type


class TypeRepository(ABC):
    @abstractmethod
    async def get_or_create_type(self, type: Type) -> Type:
        raise NotImplementedError

    @abstractmethod
    async def get_all_types(self) -> list[str]:
        raise NotImplementedError
