from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class TypeSchema(Schema):
    """Schema for storing gallery type information."""

    __tablename__ = "type"

    type: Mapped[str] = mapped_column(String, nullable=False, unique=True)
