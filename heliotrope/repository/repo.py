from typing import Any, Optional

from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import select

from heliotrope.domain.galleryinfo import HitomiGalleryinfo
from heliotrope.repository.models import Galleryinfo, mapper_registry
from heliotrope.types import HitomiGalleryinfoJSON


class _SessionManager:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def __aenter__(self) -> AsyncSession:
        self.session = sessionmaker(self.engine, AsyncSession, expire_on_commit=False)()
        return self.session

    async def __aexit__(self, *args: Any) -> None:
        await self.session.close()


class Repo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.manager = _SessionManager

    @classmethod
    async def setup(cls, db_url: str):
        engine = create_async_engine(db_url)
        async with engine.begin() as connection:
            await connection.run_sync(
                mapper_registry.metadata.create_all, checkfirst=True
            )
        return cls(engine)

    async def add_galleryinfo(self, hitomi_galleryinfo: HitomiGalleryinfo) -> None:
        async with self.manager(self.engine) as session:
            async with session.begin():
                session.add(
                    Galleryinfo.from_dict(hitomi_galleryinfo.to_dict()),
                )

        return None

    async def get_galleryinfo(
        self, galleryinfo_id: int
    ) -> Optional[HitomiGalleryinfoJSON]:
        async with self.manager(self.engine) as session:
            async with session.begin():
                r = await session.get(Galleryinfo, galleryinfo_id)
                if r:
                    return r.to_dict()

        return None

    async def get_all_index(self) -> list[int]:
        async with self.manager(self.engine) as session:
            async with session.begin():
                result = await session.execute(select(Galleryinfo.index_id))
                return [int(id) for id, in result.all()]
