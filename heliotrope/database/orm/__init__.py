"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from contextvars import ContextVar
from typing import Any, Optional

from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import mapper, relationship, selectinload
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import select

from heliotrope.abc import AbstractSQL
from heliotrope.database.orm.base import mapper_registry
from heliotrope.database.orm.table import *
from heliotrope.domain import *

_base_model_session_ctx: ContextVar[AsyncSession] = ContextVar("session")


class _SessionManager:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def __aenter__(self) -> "_SessionManager":
        self.session = sessionmaker(self.engine, AsyncSession, expire_on_commit=False)()
        self.session_ctx_token = _base_model_session_ctx.set(self.session)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if hasattr(self, "session_ctx_token"):
            _base_model_session_ctx.reset(self.session_ctx_token)
            await self.session.close()


class ORM(AbstractSQL):
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    @staticmethod
    def mapping():
        mapper(
            Galleryinfo,
            galleryinfo_table,
            properties={"files": relationship(File), "tags": relationship(Tag)},
        )
        mapper(Tag, tag_table)
        mapper(File, file_table)

    @classmethod
    async def setup(cls, db_url: str):
        cls.mapping()
        engine = create_async_engine(db_url, echo=True)
        async with engine.begin() as connection:
            await connection.run_sync(
                mapper_registry.metadata.create_all, checkfirst=True
            )
        return cls(engine)

    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> None:
        async with _SessionManager(self.engine) as manager:
            async with manager.session.begin():
                manager.session.add(galleryinfo)

        return None

    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        async with _SessionManager(self.engine) as manager:
            async with manager.session.begin():
                r = await manager.session.get(
                    Galleryinfo,
                    id,
                    [selectinload(Galleryinfo.files), selectinload(Galleryinfo.tags)],
                )
                if r:
                    return r

        return None

    async def get_all_index(self) -> list[int]:
        async with _SessionManager(self.engine) as manager:
            async with manager.session.begin():
                result = await manager.session.execute(select(Galleryinfo.id))
                return [int(id) for id, in result.all()]
