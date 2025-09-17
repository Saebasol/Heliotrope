from abc import ABC, abstractmethod


class TypeRepository(ABC):
    @abstractmethod
    async def get_all_types(self) -> list[str]:
        raise NotImplementedError
