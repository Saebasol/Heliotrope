from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String

from heliotrope.database.base import mapper_registry

file_table = Table(
    "file",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("index_id", String, ForeignKey("galleryinfo.id")),
    Column("name", String, nullable=False),
    Column("width", Integer, nullable=False),
    Column("height", Integer, nullable=False),
    Column("hash", String(64), nullable=False),
    Column("haswebp", Integer, nullable=False),
    Column("hasavifsmalltn", Integer),
    Column("hasavif", Integer),
)
