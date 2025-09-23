from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)


class SALanguageInfoRepository(LanguageInfoRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_language_info(
        self, session: AsyncSession, language_info: LanguageInfo
    ) -> LanguageInfoSchema:
        result = await session.execute(
            select(LanguageInfoSchema).where(
                and_(
                    LanguageInfoSchema.language == language_info.language,
                    LanguageInfoSchema.language_url == language_info.language_url,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        language_info_schema = LanguageInfoSchema(
            language=language_info.language,
            language_url=language_info.language_url,
        )
        session.add(language_info_schema)
        await session.flush()
        return language_info_schema

    async def get_all_language_infos(self) -> list[str]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(LanguageInfoSchema.language)
                result = await session.execute(stmt)
                return [schema for schema in result.scalars().all()]
