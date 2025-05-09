from sqlalchemy import and_, select

from heliotrope.domain.entities.character import Character
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.character import CharacterSchema


class SACharacterRepository:
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create_character(self, character: Character) -> CharacterSchema:
        async with self.sa.session_maker() as session:
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
            await session.commit()
            return schema
