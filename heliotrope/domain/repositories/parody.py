from abc import ABC, abstractmethod

from heliotrope.domain.entities.parody import Parody


class ParodyRepository(ABC):
    @abstractmethod
    async def get_or_create_parody(self, parody: Parody) -> Parody:
        raise NotImplementedError

    @abstractmethod
    async def get_all_parodies(self) -> list[str]:
        raise NotImplementedError
