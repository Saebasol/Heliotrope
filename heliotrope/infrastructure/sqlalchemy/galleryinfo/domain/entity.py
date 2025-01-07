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


class GalleryinfoSchema(Schema):
    __tablename__ = "galleryinfo"

    artists: Mapped[list[ArtistSchema]] = relationship(ArtistSchema)

    characters: Mapped[list[CharacterSchema]] = relationship(CharacterSchema)
    date: Mapped[datetime] = mapped_column(DateTime)
    # datepublished: Mapped[Optional[date_]] = mapped_column(Date)
    files: Mapped[list[FileSchema]] = relationship(FileSchema)
    galleryurl: Mapped[str] = mapped_column(String)
    groups: Mapped[list[GroupSchema]] = relationship(GroupSchema)
    japanese_title: Mapped[Optional[str]] = mapped_column(String)
    language: Mapped[str] = mapped_column(String)
    language_localname: Mapped[str] = mapped_column(String)
    languages: Mapped[list[LanguageSchema]] = relationship(LanguageSchema)
    language_url: Mapped[str] = mapped_column(String)
    parodys: Mapped[list[ParodySchema]] = relationship(ParodySchema)
    related: Mapped[list[RelatedSchema]] = relationship(RelatedSchema)
    scene_indexes: Mapped[list[SceneIndexSchema]] = relationship(SceneIndexSchema)
    tags: Mapped[list[TagSchema]] = relationship(TagSchema)
    title: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    video: Mapped[Optional[str]] = mapped_column(String)
    videofilename: Mapped[Optional[str]] = mapped_column(String)

    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    datepublished: Mapped[Optional[date_]] = mapped_column(Date, default=None)
