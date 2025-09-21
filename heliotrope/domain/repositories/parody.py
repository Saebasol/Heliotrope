from abc import ABC, abstractmethod

from heliotrope.domain.entities.parody import Parody


class ParodyRepository(ABC):
    @abstractmethod
    async def get_or_add_parody(self, parody: Parody) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_parodies(self) -> list[str]:
        raise NotImplementedError
