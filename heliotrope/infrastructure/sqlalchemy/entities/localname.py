from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class LocalnameSchema(Schema):
    """Schema for storing localized names."""

    __tablename__ = "localname"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
