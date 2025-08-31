from sqlalchemy import and_, select

from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.repositories.parody import ParodyRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.parody import ParodySchema


class SAParodyRepository(ParodyRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create_parody(self, parody: Parody) -> ParodySchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(ParodySchema).where(
                    and_(
                        ParodySchema.parody == parody.parody,
                        ParodySchema.url == parody.url,
                    )
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            schema = ParodySchema.from_dict(parody.to_dict())
            session.add(schema)
            await session.commit()
            return schema

    async def get_all_parodies(self) -> list[Parody]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(ParodySchema))
            return [Parody.from_dict(row.to_dict()) for row in result.scalars().all()]
