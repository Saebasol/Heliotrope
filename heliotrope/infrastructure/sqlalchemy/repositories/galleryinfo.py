from typing import Optional

from sqlalchemy import select, text

from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.file import FileSchema
from heliotrope.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.localname import LocalnameSchema
from heliotrope.infrastructure.sqlalchemy.entities.related import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from heliotrope.infrastructure.sqlalchemy.entities.type import TypeSchema
from heliotrope.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository
from heliotrope.infrastructure.sqlalchemy.repositories.character import (
    SACharacterRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.group import SAGroupRepository
from heliotrope.infrastructure.sqlalchemy.repositories.language import (
    SALanguageRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.localname import (
    SALocalnameRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from heliotrope.infrastructure.sqlalchemy.repositories.tag import SATagRepository
from heliotrope.infrastructure.sqlalchemy.repositories.type import SATypeRepository


class SAGalleryinfoRepository(GalleryinfoRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa
        self.type_repository = SATypeRepository(sa)
        self.artist_repository = SAArtistRepository(sa)
        self.language_info_repository = SALanguageInfoRepository(sa)
        self.localname_repository = SALocalnameRepository(sa)
        self.character_repository = SACharacterRepository(sa)
        self.group_repository = SAGroupRepository(sa)
        self.parody_repository = SAParodyRepository(sa)
        self.tag_repository = SATagRepository(sa)
        self.language_repository = SALanguageRepository(sa)

    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoSchema).where(GalleryinfoSchema.id == id)
                result = await session.execute(stmt)

                schema = result.scalar()
                if schema:
                    schema_dict = schema.to_dict()
                    return Galleryinfo.from_dict(schema_dict)
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

    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> int:
        async with self.sa.session_maker() as session:
            async with session.begin():
                type_schema = await self.type_repository.get_or_create_type(
                    TypeSchema(type=galleryinfo.type)
                )
                language_info_schema = (
                    await self.language_info_repository.get_or_create_language_info(
                        LanguageInfoSchema(
                            language=galleryinfo.language,
                            language_url=galleryinfo.language_url,
                        ),
                    )
                )
                gallery_localname_schema = (
                    await self.localname_repository.get_or_create_localname(
                        LocalnameSchema(name=galleryinfo.language_localname)
                    )
                )

                artists_schemas = [
                    await self.artist_repository.get_or_create_artist(artist)
                    for artist in galleryinfo.artists
                ]
                characters_schemas = [
                    await self.character_repository.get_or_create_character(character)
                    for character in galleryinfo.characters
                ]
                groups_schemas = [
                    await self.group_repository.get_or_create_group(group)
                    for group in galleryinfo.groups
                ]
                languages_schemas = [
                    await self.language_repository.get_or_create_language(language)
                    for language in galleryinfo.languages
                ]
                parodys_schemas = [
                    await self.parody_repository.get_or_create_parody(parody)
                    for parody in galleryinfo.parodys
                ]
                tags_schemas = [
                    await self.tag_repository.get_or_create_tag(tag)
                    for tag in galleryinfo.tags
                ]

                galleryinfo_schema = GalleryinfoSchema(
                    id=galleryinfo.id,
                    type_id=type_schema.id,
                    _type=type_schema,
                    language_info_id=language_info_schema.id,
                    _language_info=language_info_schema,
                    localname_id=gallery_localname_schema.id,
                    _localname=gallery_localname_schema,
                    date=galleryinfo.date,
                    title=galleryinfo.title,
                    japanese_title=galleryinfo.japanese_title,
                    galleryurl=galleryinfo.galleryurl,
                    video=galleryinfo.video,
                    videofilename=galleryinfo.videofilename,
                    datepublished=galleryinfo.datepublished,
                    blocked=galleryinfo.blocked,
                    artists=artists_schemas,
                    characters=characters_schemas,
                    groups=groups_schemas,
                    languages=languages_schemas,
                    parodys=parodys_schemas,
                    tags=tags_schemas,
                    related=[
                        RelatedSchema(related_id=related_id)
                        for related_id in galleryinfo.related
                    ],
                    scene_indexes=[
                        SceneIndexSchema(scene_index=scene_index)
                        for scene_index in galleryinfo.scene_indexes
                    ],
                    files=[
                        FileSchema.from_dict(file.to_dict())
                        for file in galleryinfo.files
                    ],
                )

                merged_galleryinfo = await session.merge(galleryinfo_schema)
                await session.commit()
                return merged_galleryinfo.id

    async def bulk_add_galleryinfo(self, galleryinfos: list[Galleryinfo]) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                session.add_all(
                    [GalleryinfoSchema.from_dict(g.to_dict()) for g in galleryinfos]
                )
