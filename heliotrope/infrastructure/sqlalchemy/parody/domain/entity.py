

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class ParodySchema(ForeignKeySchema):
    __tablename__ = "parody"

    parody: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
