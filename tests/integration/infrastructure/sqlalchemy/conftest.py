import json

import pytest
import pytest_asyncio

from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.base import Base
from heliotrope.infrastructure.sqlalchemy.entities.galleryinfo import (
    GalleryinfoSchema as GalleryinfoSchema,
)


@pytest.fixture()
def db_url() -> str:
    with open("tests/config.json") as f:
        config = json.load(f)
    return config["GALLERYINFO_DB_URL"]


@pytest_asyncio.fixture()
async def sqlalchemy(db_url: str):
    sqlalchemy = SQLAlchemy.create(db_url)
    await sqlalchemy.create_all_table()
    yield sqlalchemy
    async with sqlalchemy._engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await sqlalchemy.engine.dispose()
