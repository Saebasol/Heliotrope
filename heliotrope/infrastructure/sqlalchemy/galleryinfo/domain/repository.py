from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from heliotrope.core.galleryinfo.domain.entity import Galleryinfo
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.entity import (
    GalleryinfoSchema,
)
from heliotrope.core.galleryinfo.domain.repository import GalleryinfoRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy


class SAGalleryinfoRepository(GalleryinfoRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(GalleryinfoSchema)
                    .where(GalleryinfoSchema.id == id)
                    .options(
                        selectinload(GalleryinfoSchema.artists),
                        selectinload(GalleryinfoSchema.groups),
                        selectinload(GalleryinfoSchema.languages),
                        selectinload(GalleryinfoSchema.parodys),
                        selectinload(GalleryinfoSchema.related),
                        selectinload(GalleryinfoSchema.scene_indexes),
                        selectinload(GalleryinfoSchema.tags),
                        selectinload(GalleryinfoSchema.files),
                        selectinload(GalleryinfoSchema.characters),
                    )
                )

                schema = result.scalars().first()
                if schema:
                    return Galleryinfo.from_dict(schema.to_dict())
                return None

    async def get_galleryinfo_ids(self, page: int = 1, item: int = 25) -> list[int]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = (
                    select(GalleryinfoSchema.id)
                    .order_by(GalleryinfoSchema.id)
                    .limit(item)
                    .offset((page - 1) * item)
                )

                result = await session.execute(stmt)
                return list(result.scalars().all())

    async def get_all_galleryinfo_ids(self) -> list[int]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoSchema.id).order_by(GalleryinfoSchema.id)

                result = await session.execute(stmt)
                return list(result.scalars().all())

    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                session.add(GalleryinfoSchema.from_dict(galleryinfo.to_dict()))

    async def bulk_add_galleryinfo(self, galleryinfos: list[Galleryinfo]) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                session.add_all(
                    [GalleryinfoSchema.from_dict(g.to_dict()) for g in galleryinfos]
                )
