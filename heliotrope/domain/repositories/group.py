from abc import ABC, abstractmethod

from heliotrope.domain.entities.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def get_or_create_group(self, group: Group) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_all_groups(self) -> list[str]:
        raise NotImplementedError
