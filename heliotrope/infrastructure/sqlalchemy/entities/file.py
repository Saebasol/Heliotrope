from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema


class FileSchema(ForeignKeySchema):
    __tablename__ = "file"

    hasavif: Mapped[bool] = mapped_column(Boolean)
    hash: Mapped[str] = mapped_column(String)
    height: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    width: Mapped[int] = mapped_column(Integer)
    hasjxl: Mapped[bool] = mapped_column(Boolean, default=False)
    haswebp: Mapped[bool] = mapped_column(Boolean, default=False)
    single: Mapped[bool] = mapped_column(Boolean, default=False)

