from abc import ABC, abstractmethod


class GroupRepository(ABC):
    @abstractmethod
    async def get_all_groups(self) -> list[str]:
        raise NotImplementedError
