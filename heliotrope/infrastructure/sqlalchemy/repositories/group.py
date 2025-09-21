from sqlalchemy import and_, select

from heliotrope.domain.entities.group import Group
from heliotrope.domain.repositories.group import GroupRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.group import GroupSchema


class SAGroupRepository(GroupRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_group(self, group: Group) -> int:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(GroupSchema).where(
                    and_(GroupSchema.group == group.group, GroupSchema.url == group.url)
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema.id

            schema = GroupSchema.from_dict(group.to_dict())
            session.add(schema)
            await session.commit()
            return schema.id

    async def get_all_groups(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(GroupSchema.group))
            return [row for row in result.scalars().all()]
