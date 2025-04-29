from sqlalchemy import select

from heliotrope.domain.entities.language import Language
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.language import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.localname import LocalnameSchema
from heliotrope.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.repositories.localname import (
    SALocalnameRepository,
)


class SALanguageRepository:
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa
        self.language_info_repository = SALanguageInfoRepository(sa)
        self.localname_repository = SALocalnameRepository(sa)

    async def get_or_create_language(self, language: Language) -> LanguageSchema:
        language_localname_schema = (
            await self.localname_repository.get_or_create_localname(
                LocalnameSchema(name=language.language_localname)
            )
        )

        language_info_schema = (
            await self.language_info_repository.get_or_create_language_info(
                LanguageInfoSchema(
                    language=language.name,
                    language_url=f"/index-{language.name.lower()}.html",
                )
            )
        )

        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(LanguageSchema).where(
                    LanguageSchema.galleryid == language.galleryid
                    and LanguageSchema.url == language.url
                    and LanguageSchema.language_info_id == language_info_schema.id
                    and LanguageSchema.localname_id == language_localname_schema.id
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            schema = LanguageSchema(
                language_info_id=language_info_schema.id,
                localname_id=language_localname_schema.id,
                _language_info=language_info_schema,
                _localname=language_localname_schema,
                galleryid=language.galleryid,
                url=language.url,
            )
            session.add(schema)
            await session.commit()
            return schema
