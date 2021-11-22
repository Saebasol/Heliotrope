from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String

from heliotrope.database.base import mapper_registry

tag_table = Table(
    "tag",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("index_id", String, ForeignKey("galleryinfo.id")),
    Column("male", String(1)),
    Column("female", String(1)),
    Column("tag", String, nullable=False),
    Column("url", String, nullable=False),
)
