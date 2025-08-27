from abc import ABC, abstractmethod

from heliotrope.domain.entities.parody import Parody


class ParodyRepository(ABC):
    @abstractmethod
    async def get_all_parodies(self) -> list[Parody]:
        raise NotImplementedError
