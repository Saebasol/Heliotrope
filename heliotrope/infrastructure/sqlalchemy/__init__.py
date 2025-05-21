from __future__ import annotations

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

    async def create_all_table(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    def create(cls, db_url: str) -> SQLAlchemy:
        engine = create_async_engine(db_url)
        return cls(engine)
