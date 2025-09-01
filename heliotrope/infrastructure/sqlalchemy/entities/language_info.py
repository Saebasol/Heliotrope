from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class LanguageInfoSchema(Schema):
    __tablename__ = "language_info"

    language: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    language_url: Mapped[str] = mapped_column(String, nullable=False)
