from abc import ABC, abstractmethod

from heliotrope.domain.entities.artist import Artist


class ArtistRepository(ABC):
    @abstractmethod
    async def get_or_add_artist(self, artist: Artist) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_artists(self) -> list[str]:
        raise NotImplementedError
