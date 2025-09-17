from sqlalchemy import and_, select

from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.repositories.artist import ArtistRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.artist import ArtistSchema


class SAArtistRepository(ArtistRepository):
    def __init__(self, sa: SQLAlchemy):
        self.sa = sa

    async def get_or_create_artist(self, artist: Artist) -> ArtistSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(ArtistSchema).where(
                    and_(
                        ArtistSchema.artist == artist.artist,
                        ArtistSchema.url == artist.url,
                    )
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            schema = ArtistSchema.from_dict(artist.to_dict())
            session.add(schema)
            await session.commit()
            return schema

    async def get_all_artists(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(ArtistSchema.artist))
            return [row for row in result.scalars().all()]
