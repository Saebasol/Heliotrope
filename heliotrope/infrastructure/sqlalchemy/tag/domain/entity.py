from heliotrope.core.tag.domain.entity import Tag
from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column


class TagSchema(ForeignKeySchema):
    __tablename__ = "tag"

    __post_init__ = Tag.__post_init__

    tag: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    female: Mapped[bool] = mapped_column(Boolean, default=False)
    male: Mapped[bool] = mapped_column(Boolean, default=False)
