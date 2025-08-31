from sqlalchemy import and_, select

from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)


class SALanguageInfoRepository(LanguageInfoRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create_language_info(
        self, language_info_schema: LanguageInfoSchema
    ) -> LanguageInfoSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(LanguageInfoSchema).where(
                    and_(
                        LanguageInfoSchema.language == language_info_schema.language,
                        LanguageInfoSchema.language_url
                        == language_info_schema.language_url,
                    )
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            session.add(language_info_schema)
            await session.commit()
            return language_info_schema

    async def get_all_language_infos(self) -> list[LanguageInfo]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(LanguageInfoSchema)
                result = await session.execute(stmt)
                return [
                    LanguageInfo.from_dict(schema.to_dict())
                    for schema in result.scalars().all()
                ]
