

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class GroupSchema(ForeignKeySchema):
    __tablename__ = "group"

    group: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
