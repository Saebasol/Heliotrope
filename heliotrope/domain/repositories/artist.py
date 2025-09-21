from abc import ABC, abstractmethod

from heliotrope.domain.entities.artist import Artist


class ArtistRepository(ABC):
    @abstractmethod
    async def get_or_create_artist(self, artist: Artist) -> Artist:
        raise NotImplementedError

    @abstractmethod
    async def get_all_artists(self) -> list[str]:
        raise NotImplementedError
