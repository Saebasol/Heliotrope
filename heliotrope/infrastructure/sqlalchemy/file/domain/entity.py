from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column


class FileSchema(ForeignKeySchema):
    __tablename__ = "file"

    def __post_init__(self):
        self.hasavif = bool(self.hasavif)
        self.hasjxl = bool(self.hasjxl)
        self.haswebp = bool(self.haswebp)

    hasavif: Mapped[bool] = mapped_column(Boolean)
    hash: Mapped[str] = mapped_column(String)
    height: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    width: Mapped[int] = mapped_column(Integer)
    hasjxl: Mapped[bool] = mapped_column(Boolean, default=False)
    haswebp: Mapped[bool] = mapped_column(Boolean, default=False)
    single: Mapped[bool] = mapped_column(Boolean, default=False)
