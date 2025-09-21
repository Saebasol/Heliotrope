from typing import Optional

from sqlalchemy import delete, select

from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.artist import ArtistRepository
from heliotrope.domain.repositories.character import CharacterRepository
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository
from heliotrope.domain.repositories.group import GroupRepository
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.domain.repositories.language_localname import (
    LanguageLocalnameRepository,
)
from heliotrope.domain.repositories.parody import ParodyRepository
from heliotrope.domain.repositories.tag import TagRepository
from heliotrope.domain.repositories.type import TypeRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from heliotrope.infrastructure.sqlalchemy.entities.character import CharacterSchema
from heliotrope.infrastructure.sqlalchemy.entities.file import FileSchema
from heliotrope.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from heliotrope.infrastructure.sqlalchemy.entities.group import GroupSchema
from heliotrope.infrastructure.sqlalchemy.entities.language import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.parody import ParodySchema
from heliotrope.infrastructure.sqlalchemy.entities.related import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from heliotrope.infrastructure.sqlalchemy.entities.tag import TagSchema
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
                type_schema_id = await self.type_repository.get_or_add_type(
                    galleryinfo.type
                )
                language_info_schema_id = (
                    await self.language_info_repository.get_or_add_language_info(
                        galleryinfo.language_info
                    )
                )
                gallery_localname_schema_id = (
                    await self.localname_repository.get_or_add_localname(
                        galleryinfo.language_localname
                    )
                )

                artists_schemas = [
                    ArtistSchema(
                        id=await self.artist_repository.get_or_add_artist(artist),
                        artist=artist.artist,
                        url=artist.url,
                    )
                    for artist in galleryinfo.artists
                ]
                characters_schemas = [
                    CharacterSchema(
                        id=await self.character_repository.get_or_add_character(
                            character
                        ),
                        character=character.character,
                        url=character.url,
                    )
                    for character in galleryinfo.characters
                ]
                groups_schemas = [
                    GroupSchema(
                        id=await self.group_repository.get_or_add_group(group),
                        group=group.group,
                        url=group.url,
                    )
                    for group in galleryinfo.groups
                ]

                parodys_schemas = [
                    ParodySchema(
                        id=await self.parody_repository.get_or_add_parody(parody),
                        parody=parody.parody,
                        url=parody.url,
                    )
                    for parody in galleryinfo.parodys
                ]
                tags_schemas = [
                    TagSchema(
                        id=await self.tag_repository.get_or_add_tag(tag),
                        tag=tag.tag,
                        url=tag.url,
                        male=tag.male,
                        female=tag.female,
                    )
                    for tag in galleryinfo.tags
                ]

                languages_schemas: list[LanguageSchema] = []
                for language in galleryinfo.languages:
                    language_schema_language_localname_schema_id = (
                        await self.localname_repository.get_or_add_localname(
                            language.language_localname
                        )
                    )

                    language_schema_language_info_schema_id = (
                        await self.language_info_repository.get_or_add_language_info(
                            language.language_info
                        )
                    )
                    languages_schemas.append(
                        LanguageSchema(
                            galleryid=language.galleryid,
                            url=language.url,
                            language_info_id=language_schema_language_info_schema_id,
                            localname_id=language_schema_language_localname_schema_id,
                            language_info=LanguageInfoSchema(
                                id=language_schema_language_info_schema_id,
                                language=language.language_info.language,
                                language_url=language.language_info.language_url,
                            ),
                            language_localname=LanguageLocalnameSchema(
                                id=language_schema_language_localname_schema_id,
                                name=language.language_localname.name,
                            ),
                        )
                    )

                galleryinfo_schema = GalleryinfoSchema(
                    id=galleryinfo.id,
                    type_id=type_schema_id,
                    language_info_id=language_info_schema_id,
                    localname_id=gallery_localname_schema_id,
                    type=TypeSchema(id=type_schema_id, type=galleryinfo.type.type),
                    language_info=LanguageInfoSchema(
                        language=galleryinfo.language_info.language,
                        language_url=galleryinfo.language_info.language_url,
                        id=language_info_schema_id,
                    ),
                    language_localname=LanguageLocalnameSchema(
                        name=galleryinfo.language_localname.name,
                        id=gallery_localname_schema_id,
                    ),
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

                await session.merge(galleryinfo_schema)
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
