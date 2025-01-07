from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema


class ArtistSchema(ForeignKeySchema):
    __tablename__ = "artist"

    artist: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
