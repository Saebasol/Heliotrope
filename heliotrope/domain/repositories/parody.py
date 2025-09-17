from abc import ABC, abstractmethod


class ParodyRepository(ABC):
    @abstractmethod
    async def get_all_parodies(self) -> list[str]:
        raise NotImplementedError
