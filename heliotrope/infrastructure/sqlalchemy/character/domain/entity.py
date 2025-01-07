from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from dataclasses import dataclass

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema


@dataclass
class CharacterSchema(ForeignKeySchema):
    __tablename__ = "character"

    character: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
