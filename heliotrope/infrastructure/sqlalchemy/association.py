from sqlalchemy import Column, ForeignKey, Integer, Table

from heliotrope.infrastructure.sqlalchemy.base import Base

galleryinfo_id = lambda: Column("galleryinfo_id", Integer, ForeignKey("galleryinfo.id"))

galleryinfo_artist = Table(
    "galleryinfo_artist",
    Base.metadata,
    galleryinfo_id(),
    Column("artist_id", Integer, ForeignKey("artist.id", ondelete="RESTRICT")),
)

galleryinfo_character = Table(
    "galleryinfo_character",
    Base.metadata,
    galleryinfo_id(),
    Column("character_id", Integer, ForeignKey("character.id", ondelete="RESTRICT")),
)

galleryinfo_group = Table(
    "galleryinfo_group",
    Base.metadata,
    galleryinfo_id(),
    Column("group_id", Integer, ForeignKey("group.id", ondelete="RESTRICT")),
)

galleryinfo_parody = Table(
    "galleryinfo_parody",
    Base.metadata,
    galleryinfo_id(),
    Column("parody_id", Integer, ForeignKey("parody.id", ondelete="RESTRICT")),
)

galleryinfo_tag = Table(
    "galleryinfo_tag",
    Base.metadata,
    galleryinfo_id(),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="RESTRICT")),
)

galleryinfo_language = Table(
    "galleryinfo_language",
    Base.metadata,
    galleryinfo_id(),
    Column("language_id", Integer, ForeignKey("language.id", ondelete="RESTRICT")),
)
