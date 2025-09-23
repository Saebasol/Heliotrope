from typing import Optional

from sqlalchemy import delete, select

from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.file import FileSchema
from heliotrope.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from heliotrope.infrastructure.sqlalchemy.entities.language import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.entities.related import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from heliotrope.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository
from heliotrope.infrastructure.sqlalchemy.repositories.character import (
    SACharacterRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.group import SAGroupRepository
from heliotrope.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.language_localname import (
    SALanguageLocalnameRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from heliotrope.infrastructure.sqlalchemy.repositories.tag import SATagRepository
from heliotrope.infrastructure.sqlalchemy.repositories.type import SATypeRepository


class SAGalleryinfoRepository(GalleryinfoRepository):
    def __init__(
        self,
        sa: SQLAlchemy,
        type_repository: SATypeRepository,
        artist_repository: SAArtistRepository,
        language_info_repository: SALanguageInfoRepository,
        localname_repository: SALanguageLocalnameRepository,
        character_repository: SACharacterRepository,
        group_repository: SAGroupRepository,
        parody_repository: SAParodyRepository,
        tag_repository: SATagRepository,
    ) -> None:
        self.sa = sa
        self.type_repository = type_repository
        self.artist_repository = artist_repository
        self.language_info_repository = language_info_repository
        self.localname_repository = localname_repository
        self.character_repository = character_repository
        self.group_repository = group_repository
        self.parody_repository = parody_repository
        self.tag_repository = tag_repository

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

    async def get_all_galleryinfo_ids(self) -> list[int]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoSchema.id).order_by(GalleryinfoSchema.id)
                result = await session.execute(stmt)
                return list(result.scalars().all())

    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> int:
        async with self.sa.session_maker() as session:
            async with session.begin():
                type_schema = await self.type_repository.get_or_add_type(
                    session, galleryinfo.type
                )
                language_info_schema = (
                    await self.language_info_repository.get_or_add_language_info(
                        session, galleryinfo.language_info
                    )
                )
                language_localname_schema = (
                    await self.localname_repository.get_or_add_language_localname(
                        session, galleryinfo.language_localname
                    )
                )

                artists_schemas = [
                    await self.artist_repository.get_or_add_artist(session, artist)
                    for artist in galleryinfo.artists
                ]
                characters_schemas = [
                    await self.character_repository.get_or_add_character(
                        session, character
                    )
                    for character in galleryinfo.characters
                ]

                groups_schemas = [
                    await self.group_repository.get_or_add_group(session, group)
                    for group in galleryinfo.groups
                ]

                parodys_schemas = [
                    await self.parody_repository.get_or_add_parody(session, parody)
                    for parody in galleryinfo.parodys
                ]

                tags_schemas = [
                    await self.tag_repository.get_or_add_tag(session, tag)
                    for tag in galleryinfo.tags
                ]

                languages_schemas: list[LanguageSchema] = []
                for language in galleryinfo.languages:
                    language_language_localname_schema = (
                        await self.localname_repository.get_or_add_language_localname(
                            session, language.language_localname
                        )
                    )

                    language_language_info_schema = (
                        await self.language_info_repository.get_or_add_language_info(
                            session, language.language_info
                        )
                    )
                    languages_schemas.append(
                        LanguageSchema(
                            galleryid=language.galleryid,
                            url=language.url,
                            language_info_id=language_language_info_schema.id,
                            localname_id=language_language_localname_schema.id,
                            language_info=language_info_schema,
                            language_localname=language_localname_schema,
                        )
                    )

                galleryinfo_schema = GalleryinfoSchema(
                    id=galleryinfo.id,
                    type_id=type_schema.id,
                    language_info_id=language_info_schema.id,
                    localname_id=language_localname_schema.id,
                    type=type_schema,
                    language_info=language_info_schema,
                    language_localname=language_localname_schema,
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
                    parodys=parodys_schemas,
                    tags=tags_schemas,
                    languages=languages_schemas,
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

                session.add(galleryinfo_schema)
                await session.commit()
                return galleryinfo_schema.id

    async def is_galleryinfo_exists(self, id: int) -> bool:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(1).where(GalleryinfoSchema.id == id)
                result = await session.execute(stmt)
                return result.scalar() is not None

    async def delete_galleryinfo(self, id: int) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = delete(GalleryinfoSchema).where(GalleryinfoSchema.id == id)
                await session.execute(stmt)
