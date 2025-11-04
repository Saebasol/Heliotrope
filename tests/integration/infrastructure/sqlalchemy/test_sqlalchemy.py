import pytest
from sqlalchemy import Connection, inspect
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities import (
    GalleryinfoSchema as GalleryinfoSchema,
)


@pytest.mark.asyncio
async def test_create_all_tables(db_url: str):
    sqlalchemy = SQLAlchemy.create(db_url)
    await sqlalchemy.create_all_table()

    async with sqlalchemy._engine.connect() as conn:

        def get_tables(sync_conn: Connection):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        tables = await conn.run_sync(get_tables)
        assert tables
