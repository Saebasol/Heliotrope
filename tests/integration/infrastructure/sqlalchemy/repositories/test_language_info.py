from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from tests.unit.domain.entities.conftest import (
    sample_language_info as sample_language_info,
)


@pytest.mark.asyncio
async def test_get_or_add_language_info_new_language_info(
    sample_language_info: LanguageInfo,
    language_info_repository: SALanguageInfoRepository,
    session: AsyncSession,
):
    language_info_id = await language_info_repository.get_or_add_language_info(
        session, sample_language_info
    )

    assert language_info_id is not None
    assert isinstance(language_info_id, int)
    assert language_info_id > 0


@pytest.mark.asyncio
async def test_get_or_add_language_info_existing_language_info(
    sample_language_info: LanguageInfo,
    language_info_repository: SALanguageInfoRepository,
    session: AsyncSession,
):
    first_id = await language_info_repository.get_or_add_language_info(
        session, sample_language_info
    )
    second_id = await language_info_repository.get_or_add_language_info(
        session, sample_language_info
    )

    assert first_id == second_id


@pytest.mark.asyncio
async def test_get_all_language_info_with_data(
    sample_language_info: LanguageInfo,
    language_info_repository: SALanguageInfoRepository,
    session: AsyncSession,
):
    language_info1 = sample_language_info
    language_info1.language = "English"
    language_info1.language_url = "/language/english.html"
    language_info2 = deepcopy(sample_language_info)
    language_info2.language = "Spanish"
    language_info2.language_url = "/language/spanish.html"
    language_info3 = deepcopy(sample_language_info)
    language_info3.language = "Japanese"
    language_info3.language_url = "/language/japanese.html"

    await language_info_repository.get_or_add_language_info(session, language_info1)
    await language_info_repository.get_or_add_language_info(session, language_info2)
    await language_info_repository.get_or_add_language_info(session, language_info3)

    languages = await language_info_repository.get_all_language_infos()
    assert len(languages) == 3
    assert "English" in languages
    assert "Spanish" in languages
    assert "Japanese" in languages
