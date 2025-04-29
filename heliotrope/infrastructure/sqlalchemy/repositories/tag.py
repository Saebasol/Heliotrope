from sqlalchemy import select, and_

from heliotrope.domain.entities.tag import Tag
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.tag import TagSchema


class SATagRepository:
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create_tag(self, tag: Tag) -> TagSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(TagSchema).where(
                    and_(
                        TagSchema.tag == tag.tag,
                        TagSchema.url == tag.url,
                        TagSchema.female == tag.female,
                        TagSchema.male == tag.male,
                    )
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            schema = TagSchema.from_dict(tag.to_dict())
            session.add(schema)
            await session.commit()
            return schema
