from sqlalchemy import select

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

    async def get_or_create_localname(
        self, localname_schema: LanguageLocalnameSchema
    ) -> LanguageLocalnameSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(LanguageLocalnameSchema).where(
                    LanguageLocalnameSchema.name == localname_schema.name
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            session.add(localname_schema)
            await session.commit()
            return localname_schema
