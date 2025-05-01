from dataclasses import field

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import reconstructor  # pyright: ignore[reportUnknownVariableType]
from sqlalchemy.orm import Mapped, mapped_column, relationship

from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.localname import LocalnameSchema
from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class LanguageSchema(Schema):
    """Schema for storing language information."""

    __tablename__ = "language"

    def __post_init__(self) -> None:
        self.name = self._language_info.language
        self.language_localname = self._localname.name

    @reconstructor
    def init_on_load(self) -> None:
        self.__post_init__()

    # 외래 키 관계
    language_info_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("language_info.id", ondelete="RESTRICT"), nullable=False
    )
    localname_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("localname.id", ondelete="RESTRICT"), nullable=False
    )

    galleryid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    url: Mapped[str] = mapped_column(String)

    _language_info: Mapped[LanguageInfoSchema] = relationship(
        LanguageInfoSchema,
        lazy="selectin",
        uselist=False,
    )

    _localname: Mapped[LocalnameSchema] = relationship(
        LocalnameSchema,
        lazy="selectin",
        uselist=False,
    )

    name: str = field(init=False)
    language_localname: str = field(init=False)
