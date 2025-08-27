from abc import ABC, abstractmethod

from heliotrope.domain.entities.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def get_all_groups(self) -> list[Group]:
        raise NotImplementedError
