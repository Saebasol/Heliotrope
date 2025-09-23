from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.artist import Artist
from heliotrope.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from heliotrope.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository
from tests.unit.domain.entities.conftest import sample_artist as sample_artist


@pytest.mark.asyncio
async def test_get_or_add_artist_new_artist(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    artist = await artist_repository.get_or_add_artist(session, sample_artist)

    assert artist is not None
    assert isinstance(artist, ArtistSchema)


@pytest.mark.asyncio
async def test_get_or_add_artist_existing_artist(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    first = await artist_repository.get_or_add_artist(session, sample_artist)
    second = await artist_repository.get_or_add_artist(session, sample_artist)

    await session.commit()

    assert first == second


@pytest.mark.asyncio
async def test_get_all_artists_with_data(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    artist1 = sample_artist
    artist1.artist = "artist_one"
    artist1.url = "/artist/one.html"
    artist2 = deepcopy(sample_artist)
    artist2.artist = "artist_two"
    artist2.url = "/artist/two.html"
    artist3 = deepcopy(sample_artist)
    artist3.artist = "artist_three"
    artist3.url = "/artist/three.html"

    await artist_repository.get_or_add_artist(session, artist1)
    await artist_repository.get_or_add_artist(session, artist2)
    await artist_repository.get_or_add_artist(session, artist3)

    await session.commit()

    artists = await artist_repository.get_all_artists()

    assert len(artists) == 3
    assert "artist_one" in artists
    assert "artist_two" in artists
    assert "artist_three" in artists
