from sqlalchemy import select

from heliotrope.domain.entities.type import Type
from heliotrope.domain.repositories.type import TypeRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.type import TypeSchema


class SATypeRepository(TypeRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_type(self, type: Type) -> int:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(TypeSchema).where(TypeSchema.type == type.type)
            )
            schema = result.scalars().first()

            if schema:
                return schema.id

            type_schema = TypeSchema.from_dict(type.to_dict())
            session.add(type_schema)
            await session.commit()
            return type_schema.id

    async def get_all_types(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(TypeSchema.type))
            return [row for row in result.scalars().all()]
