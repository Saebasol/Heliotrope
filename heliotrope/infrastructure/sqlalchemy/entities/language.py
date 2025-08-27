from dataclasses import field

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class LanguageSchema(Schema):
    """Schema for storing language information."""

    __tablename__ = "language"

    # 외래 키 관계
    language_info_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("language_info.id", ondelete="RESTRICT"), nullable=False
    )
    localname_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("localname.id", ondelete="RESTRICT"), nullable=False
    )

    galleryid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    url: Mapped[str] = mapped_column(String)

    language_info: Mapped[LanguageInfoSchema] = relationship(
        LanguageInfoSchema,
        lazy="selectin",
        uselist=False,
    )

    localname: Mapped[LanguageLocalnameSchema] = relationship(
        LanguageLocalnameSchema,
        lazy="selectin",
        uselist=False,
    )

    name: str = field(init=False)
    language_localname: str = field(init=False)
