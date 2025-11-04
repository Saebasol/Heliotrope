import pytest_asyncio
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.character import (
    SACharacterRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.group import SAGroupRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.language_localname import (
    SALanguageLocalnameRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.tag import SATagRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.type import SATypeRepository

from tests.unit.domain.entities.conftest import *


@pytest_asyncio.fixture()
async def session(sqlalchemy: SQLAlchemy):
    async with sqlalchemy.session_maker() as session:
        yield session


@pytest_asyncio.fixture()
async def artist_repository(sqlalchemy: SQLAlchemy):
    return SAArtistRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def character_repository(sqlalchemy: SQLAlchemy):
    return SACharacterRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def group_repository(sqlalchemy: SQLAlchemy):
    return SAGroupRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def language_info_repository(sqlalchemy: SQLAlchemy):
    return SALanguageInfoRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def language_localname_repository(sqlalchemy: SQLAlchemy):
    return SALanguageLocalnameRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def parody_repository(sqlalchemy: SQLAlchemy):
    return SAParodyRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def tag_repository(sqlalchemy: SQLAlchemy):
    return SATagRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def type_repository(sqlalchemy: SQLAlchemy):
    return SATypeRepository(sqlalchemy)


@pytest_asyncio.fixture()
async def galleryinfo_repository(
    sqlalchemy: SQLAlchemy,
    language_info_repository: SALanguageInfoRepository,
    artist_repository: SAArtistRepository,
    character_repository: SACharacterRepository,
    group_repository: SAGroupRepository,
    parody_repository: SAParodyRepository,
    tag_repository: SATagRepository,
    type_repository: SATypeRepository,
    language_localname_repository: SALanguageLocalnameRepository,
):
    return SAGalleryinfoRepository(
        sqlalchemy,
        type_repository=type_repository,
        artist_repository=artist_repository,
        language_info_repository=language_info_repository,
        localname_repository=language_localname_repository,
        character_repository=character_repository,
        group_repository=group_repository,
        parody_repository=parody_repository,
        tag_repository=tag_repository,
    )
