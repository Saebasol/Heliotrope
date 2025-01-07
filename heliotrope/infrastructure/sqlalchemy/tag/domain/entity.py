from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column


class TagSchema(ForeignKeySchema):
    __tablename__ = "tag"

    tag: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    female: Mapped[bool] = mapped_column(Boolean, default=False)
    male: Mapped[bool] = mapped_column(Boolean, default=False)
