import pytest
from sqlalchemy import text

from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities import (
    GalleryinfoSchema as GalleryinfoSchema,
)


@pytest.mark.asyncio
async def test_create_all_tables(db_url: str):
    sqlalchemy = SQLAlchemy.create(db_url)
    await sqlalchemy.create_all_table()

    async with sqlalchemy.engine.connect() as conn:
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        table_names = [row[0] for row in result.fetchall()]
        assert len(table_names) > 0
