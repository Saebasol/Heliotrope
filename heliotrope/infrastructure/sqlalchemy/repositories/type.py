from sqlalchemy import select

from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.type import TypeSchema


class SATypeRepository:
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create_type(self, type_schema: TypeSchema) -> TypeSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(TypeSchema).where(TypeSchema.type == type_schema.type)
            )
            schema = result.scalars().first()

            if schema:
                return schema

            session.add(type_schema)
            await session.commit()
            return type_schema

    async def get_all_types(self) -> list[TypeSchema]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(TypeSchema))
            return list(result.scalars().all())
