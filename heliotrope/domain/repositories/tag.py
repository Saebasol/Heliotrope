from abc import ABC, abstractmethod


class TagRepository(ABC):
    @abstractmethod
    async def get_all_tags(self) -> list[tuple[str, bool, bool]]:
        raise NotImplementedError
