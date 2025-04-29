from sqlalchemy import select

from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.localname import LocalnameSchema


class SALocalnameRepository:
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create_localname(
        self, localname_schema: LocalnameSchema
    ) -> LocalnameSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(LocalnameSchema).where(
                    LocalnameSchema.name == localname_schema.name
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            session.add(localname_schema)
            await session.commit()
            return localname_schema
