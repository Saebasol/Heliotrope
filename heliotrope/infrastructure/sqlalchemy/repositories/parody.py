from sqlalchemy import select, and_

from heliotrope.domain.entities.parody import Parody
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.parody import ParodySchema


class SAParodyRepository:
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
