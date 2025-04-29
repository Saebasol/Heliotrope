from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class TagSchema(Schema):
    __tablename__ = "tag"

    tag: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    female: Mapped[bool] = mapped_column(Boolean, default=False)
    male: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("tag", "female", "male"),)
