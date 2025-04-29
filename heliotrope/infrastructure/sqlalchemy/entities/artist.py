from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import Schema


class ArtistSchema(Schema):
    __tablename__ = "artist"

    artist: Mapped[str] = mapped_column(String, unique=True)
    url: Mapped[str] = mapped_column(String)
