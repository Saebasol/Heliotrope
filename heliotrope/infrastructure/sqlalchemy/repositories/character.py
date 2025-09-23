from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.character import Character
from heliotrope.domain.repositories.character import CharacterRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.character import CharacterSchema


class SACharacterRepository(CharacterRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_character(
        self, session: AsyncSession, character: Character
    ) -> CharacterSchema:
        result = await session.execute(
            select(CharacterSchema).where(
                and_(
                    CharacterSchema.character == character.character,
                    CharacterSchema.url == character.url,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        schema = CharacterSchema.from_dict(character.to_dict())
        session.add(schema)
        await session.flush()
        return schema

    async def get_all_characters(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(CharacterSchema.character))
            return [row for row in result.scalars().all()]
