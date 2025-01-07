from typing import Optional
from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class LanguageSchema(ForeignKeySchema):
    __tablename__ = "language"

    language_localname: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    galleryid: Mapped[Optional[int]] = mapped_column(
        Integer, default=None, nullable=True
    )
