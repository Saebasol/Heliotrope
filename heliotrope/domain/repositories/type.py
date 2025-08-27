from abc import ABC, abstractmethod

from heliotrope.domain.entities.type import Type


class TypeRepository(ABC):
    @abstractmethod
    async def get_all_types(self) -> list[Type]:
        raise NotImplementedError
