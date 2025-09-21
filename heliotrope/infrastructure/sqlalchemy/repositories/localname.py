from sqlalchemy import select

from heliotrope.domain.entities.language_localname import LanguageLocalname
from heliotrope.domain.repositories.language_localname import (
    LanguageLocalnameRepository,
)
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)


class SALanguageLocalnameRepository(LanguageLocalnameRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_localname(self, localname: LanguageLocalname) -> int:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(LanguageLocalnameSchema).where(
                    LanguageLocalnameSchema.name == localname.name
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema.id

            localname_schema = LanguageLocalnameSchema.from_dict(localname.to_dict())
            session.add(localname_schema)
            await session.commit()
            return localname_schema.id
