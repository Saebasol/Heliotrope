from heliotrope.domain.entities.language import Language
from heliotrope.domain.repositories.language import LanguageRepository
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.domain.repositories.language_localname import (
    LanguageLocalnameRepository,
)
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.entities.language import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)


class SALanguageRepository(LanguageRepository):
    def __init__(
        self,
        sa: SQLAlchemy,
        language_info_repository: LanguageInfoRepository,
        language_localname_repository: LanguageLocalnameRepository,
    ) -> None:
        self.sa = sa
        self.language_info_repository = language_info_repository
        self.language_localname_repository = language_localname_repository

    async def create_language(self, language: Language) -> LanguageSchema:
        language_localname_schema = (
            await self.language_localname_repository.get_or_create_localname(
                LanguageLocalnameSchema.from_dict(language.language_localname.to_dict())
            )
        )

        language_info_schema = await self.language_info_repository.get_or_create_language_info(
            LanguageInfoSchema(
                language=language.language_info.language,
                language_url=f"/index-{language.language_info.language.lower()}.html",
            )
        )

        schema = LanguageSchema(
            language_info_id=language_info_schema.id,
            localname_id=language_localname_schema.id,
            language_info=language_info_schema,
            language_localname=language_localname_schema,
            galleryid=language.galleryid,
            url=language.url,
        )
        return schema
