from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import String

from heliotrope.database.base import mapper_registry

galleryinfo_table = Table(
    "galleryinfo",
    mapper_registry.metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("title", String, nullable=False),
    Column("japanese_title", String),
    Column("language", String, nullable=False),
    Column("language_localname", String, nullable=False),
    Column("type", String, nullable=False),
    Column("date", String, nullable=False),
)
