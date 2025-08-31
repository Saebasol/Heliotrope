from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class LanguageLocalnameSchema(Schema):
    """Schema for storing localized names."""

    __tablename__ = "language_localname"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
