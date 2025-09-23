import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.language_localname import LanguageLocalname
from heliotrope.infrastructure.sqlalchemy.repositories.language_localname import (
    SALanguageLocalnameRepository,
)
from tests.unit.domain.entities.conftest import (
    sample_language_localname as sample_language_localname,
)


@pytest.mark.asyncio
async def test_get_or_add_language_localname_new_language_localname(
    sample_language_localname: LanguageLocalname,
    language_localname_repository: SALanguageLocalnameRepository,
    session: AsyncSession,
):
    language_localname_id = (
        await language_localname_repository.get_or_add_language_localname(
            session, sample_language_localname
        )
    )

    assert language_localname_id is not None
    assert isinstance(language_localname_id, int)
    assert language_localname_id > 0


@pytest.mark.asyncio
async def test_get_or_add_language_localname_existing_language_localname(
    sample_language_localname: LanguageLocalname,
    language_localname_repository: SALanguageLocalnameRepository,
    session: AsyncSession,
):
    first_id = await language_localname_repository.get_or_add_language_localname(
        session, sample_language_localname
    )
    second_id = await language_localname_repository.get_or_add_language_localname(
        session, sample_language_localname
    )

    assert first_id == second_id
