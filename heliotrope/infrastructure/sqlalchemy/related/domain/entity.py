from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class RelatedSchema(ForeignKeySchema):
    __tablename__ = "related"

    related_id: Mapped[int] = mapped_column(Integer)
