from heliotrope.infrastructure.sqlalchemy.mixin import ForeignKeySchema
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column


class TagSchema(ForeignKeySchema):
    __tablename__ = "tag"

    def __post_init__(self):
        if self.female in ["0", 0, None, ""]:
            self.female = False

        if self.female in ["1", 1]:
            self.female = True

        if self.male in ["0", 0, None, ""]:
            self.male = False

        if self.male in ["1", 1]:
            self.male = True

    tag: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    female: Mapped[bool] = mapped_column(Boolean, default=False)
    male: Mapped[bool] = mapped_column(Boolean, default=False)
