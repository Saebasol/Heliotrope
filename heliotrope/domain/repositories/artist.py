from abc import ABC, abstractmethod

from heliotrope.domain.entities.artist import Artist


class ArtistRepository(ABC):

    @abstractmethod
    async def get_all_artists(self) -> list[Artist]:
        raise NotImplementedError
