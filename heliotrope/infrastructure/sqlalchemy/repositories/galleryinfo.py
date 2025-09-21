from typing import Optional

from sqlalchemy import delete, select

from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.artist import ArtistRepository
from heliotrope.domain.repositories.character import CharacterRepository
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository
from heliotrope.domain.repositories.group import GroupRepository
from heliotrope.domain.repositories.language import LanguageRepository
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.domain.repositories.language_localname import (
    LanguageLocalnameRepository,
)
from heliotrope.domain.repositories.parody import ParodyRepository
from heliotrope.domain.repositories.tag import TagRepository
from heliotrope.domain.repositories.type import TypeRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.file import FileSchema
from heliotrope.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.related import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from heliotrope.infrastructure.sqlalchemy.entities.type import TypeSchema


class SAGalleryinfoRepository(GalleryinfoRepository):
    def __init__(
        self,
        sa: SQLAlchemy,
        type_repository: TypeRepository,
        artist_repository: ArtistRepository,
        language_info_repository: LanguageInfoRepository,
        localname_repository: LanguageLocalnameRepository,
        character_repository: CharacterRepository,
        group_repository: GroupRepository,
        parody_repository: ParodyRepository,
        tag_repository: TagRepository,
        language_repository: LanguageRepository,
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
        self.language_repository = language_repository

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
                type_schema = await self.type_repository.get_or_create_type(
                    TypeSchema.from_dict(galleryinfo.type.to_dict())
                )
                language_info_schema = (
                    await self.language_info_repository.get_or_create_language_info(
                        LanguageInfoSchema.from_dict(
                            galleryinfo.language_info.to_dict()
                        )
                    )
                )
                gallery_localname_schema = (
                    await self.localname_repository.get_or_create_localname(
                        LanguageLocalnameSchema.from_dict(
                            galleryinfo.language_localname.to_dict()
                        )
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
                    await self.language_repository.create_language(language)
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
                    language_info_id=language_info_schema.id,
                    localname_id=gallery_localname_schema.id,
                    type=type_schema,
                    language_info=language_info_schema,
                    language_localname=gallery_localname_schema,
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
