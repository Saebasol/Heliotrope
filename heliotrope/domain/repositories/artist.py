from abc import ABC, abstractmethod


class ArtistRepository(ABC):
    @abstractmethod
    async def get_all_artists(self) -> list[str]:
        raise NotImplementedError
