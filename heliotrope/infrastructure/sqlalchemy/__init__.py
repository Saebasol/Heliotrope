from __future__ import annotations

from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from heliotrope.infrastructure.sqlalchemy.base import Base


class SQLAlchemy:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._session_maker = async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )
        self._current_session: ContextVar[AsyncSession | None] = ContextVar(
            "current_session", default=None
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._session_maker

    @classmethod
    async def create(cls, db_url: str) -> SQLAlchemy:
        engine = create_async_engine(db_url)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        return cls(engine)
