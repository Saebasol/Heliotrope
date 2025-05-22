from dataclasses import field
from datetime import date as date_
from datetime import datetime
from functools import partial
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from heliotrope.infrastructure.sqlalchemy.association import (
    galleryinfo_artist,
    galleryinfo_character,
    galleryinfo_group,
    galleryinfo_language,
    galleryinfo_parody,
    galleryinfo_tag,
)
from heliotrope.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from heliotrope.infrastructure.sqlalchemy.entities.character import CharacterSchema
from heliotrope.infrastructure.sqlalchemy.entities.file import FileSchema
from heliotrope.infrastructure.sqlalchemy.entities.group import GroupSchema
from heliotrope.infrastructure.sqlalchemy.entities.language import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.localname import LocalnameSchema
from heliotrope.infrastructure.sqlalchemy.entities.parody import ParodySchema
from heliotrope.infrastructure.sqlalchemy.entities.related import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from heliotrope.infrastructure.sqlalchemy.entities.tag import TagSchema
from heliotrope.infrastructure.sqlalchemy.entities.type import TypeSchema
from heliotrope.infrastructure.sqlalchemy.mixin import Schema

one_to_many_relationship = partial(
    relationship,
    cascade="all, delete-orphan",
    passive_deletes=True,
    lazy="selectin",
)

many_to_many_relationship = partial(
    relationship,
    passive_deletes=True,
    lazy="selectin",
)
many_to_one_relationship = partial(
    relationship,
    uselist=False,
    lazy="joined",
)


class GalleryinfoSchema(Schema):
    __tablename__ = "galleryinfo"

    def __post_init__(self) -> None:
        self.type = self._type.type
        self.language = self._language_info.language
        self.language_url = self._language_info.language_url
        self.language_localname = self._localname.name

    @reconstructor
    def init_on_load(self) -> None:
        self.__post_init__()

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    japanese_title: Mapped[Optional[str]] = mapped_column(String)
    galleryurl: Mapped[str] = mapped_column(String, nullable=False)
    video: Mapped[Optional[str]] = mapped_column(String)
    videofilename: Mapped[Optional[str]] = mapped_column(String)

    type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("type.id", ondelete="RESTRICT"), nullable=True
    )
    language_info_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("language_info.id", ondelete="RESTRICT"), nullable=True
    )
    localname_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("localname.id", ondelete="RESTRICT"), nullable=True
    )

    datepublished: Mapped[Optional[date_]] = mapped_column(Date, default=None)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    artists: Mapped[list[ArtistSchema]] = many_to_many_relationship(
        ArtistSchema,
        secondary=galleryinfo_artist,
    )
    characters: Mapped[list[CharacterSchema]] = many_to_many_relationship(
        CharacterSchema,
        secondary=galleryinfo_character,
    )

    groups: Mapped[list[GroupSchema]] = many_to_many_relationship(
        GroupSchema,
        secondary=galleryinfo_group,
    )
    languages: Mapped[list[LanguageSchema]] = many_to_many_relationship(
        LanguageSchema,
        secondary=galleryinfo_language,
    )
    parodys: Mapped[list[ParodySchema]] = many_to_many_relationship(
        ParodySchema,
        secondary=galleryinfo_parody,
    )
    tags: Mapped[list[TagSchema]] = many_to_many_relationship(
        TagSchema,
        secondary=galleryinfo_tag,
    )

    related: Mapped[list[RelatedSchema]] = one_to_many_relationship(RelatedSchema)
    scene_indexes: Mapped[list[SceneIndexSchema]] = one_to_many_relationship(
        SceneIndexSchema
    )
    files: Mapped[list[FileSchema]] = one_to_many_relationship(FileSchema)

    _type: Mapped[TypeSchema] = many_to_one_relationship(
        TypeSchema, uselist=False, lazy="joined"
    )

    _language_info: Mapped[LanguageInfoSchema] = many_to_one_relationship(
        LanguageInfoSchema, uselist=False, lazy="joined"
    )

    _localname: Mapped[LocalnameSchema] = many_to_one_relationship(
        LocalnameSchema, uselist=False, lazy="joined"
    )

    type: str = field(init=False)

    language: str = field(init=False)

    language_url: str = field(init=False)

    language_localname: str = field(init=False)
