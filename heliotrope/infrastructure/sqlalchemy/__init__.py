from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from heliotrope.infrastructure.sqlalchemy.base import Base


class SQLAlchemy:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

    @classmethod
    async def create(cls, db_url: str) -> SQLAlchemy:
        engine = create_async_engine(db_url)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all, checkfirst=True)
        return cls(engine)
