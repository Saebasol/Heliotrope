from datetime import datetime, date as date_
from typing import Optional
from sqlalchemy import Boolean, String, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from heliotrope.infrastructure.sqlalchemy.artist.domain.entity import ArtistSchema
from heliotrope.infrastructure.sqlalchemy.character.domain.entity import CharacterSchema
from heliotrope.infrastructure.sqlalchemy.file.domain.entity import FileSchema
from heliotrope.infrastructure.sqlalchemy.group.domain.entity import GroupSchema
from heliotrope.infrastructure.sqlalchemy.language.domain.entity import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.mixin import Schema
from heliotrope.infrastructure.sqlalchemy.parody.domain.entity import ParodySchema
from heliotrope.infrastructure.sqlalchemy.related.domain.entity import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.tag.domain.entity import TagSchema
from heliotrope.infrastructure.sqlalchemy.scene_index.domain.entity import (
    SceneIndexSchema,
)

from functools import partial

relationship = partial(
    relationship,
    cascade="all, delete",
    passive_deletes=True,
)


class GalleryinfoSchema(Schema):
    """
    Schema for storing gallery information with related entities and metadata.
    """

    __tablename__ = "galleryinfo"

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    japanese_title: Mapped[Optional[str]] = mapped_column(String)
    galleryurl: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    language_localname: Mapped[str] = mapped_column(String, nullable=False)
    language_url: Mapped[str] = mapped_column(String, nullable=False)
    video: Mapped[Optional[str]] = mapped_column(String)
    videofilename: Mapped[Optional[str]] = mapped_column(String)

    # Relationships
    artists: Mapped[list[ArtistSchema]] = relationship(ArtistSchema)
    characters: Mapped[list[CharacterSchema]] = relationship(CharacterSchema)
    files: Mapped[list[FileSchema]] = relationship(FileSchema)
    groups: Mapped[list[GroupSchema]] = relationship(GroupSchema)
    languages: Mapped[list[LanguageSchema]] = relationship(LanguageSchema)
    parodys: Mapped[list[ParodySchema]] = relationship(ParodySchema)
    related: Mapped[list[RelatedSchema]] = relationship(RelatedSchema)
    scene_indexes: Mapped[list[SceneIndexSchema]] = relationship(SceneIndexSchema)
    tags: Mapped[list[TagSchema]] = relationship(TagSchema)

    datepublished: Mapped[Optional[date_]] = mapped_column(Date, default=None)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
