from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema


class SceneIndexSchema(ForeignKeySchema):
    __tablename__ = "scene_index"

    scene_index: Mapped[int] = mapped_column(Integer)
