from abc import ABC, abstractmethod

from heliotrope.domain.entities.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def get_or_add_group(self, group: Group) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_groups(self) -> list[str]:
        raise NotImplementedError
