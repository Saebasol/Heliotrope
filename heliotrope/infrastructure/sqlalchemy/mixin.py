from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


from heliotrope.infrastructure.sqlalchemy.serializer import SchemaSerializer
from heliotrope.infrastructure.sqlalchemy.base import Base
from heliotrope.infrastructure.sqlalchemy.deserializer import SchemaDeserializer


class Schema(Base, SchemaDeserializer, SchemaSerializer, kw_only=True):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, default=None, kw_only=True
    )


class ForeignKeySchema(Schema):
    __abstract__ = True
    galleryinfo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("galleryinfo.id", ondelete="CASCADE"),
        nullable=False,
        default=None,
        kw_only=True,
        index=True,
    )
