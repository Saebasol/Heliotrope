import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.tag import Tag
from heliotrope.infrastructure.sqlalchemy.repositories.tag import SATagRepository
from tests.unit.domain.entities.conftest import sample_artist as sample_artist


@pytest.mark.asyncio
async def test_get_or_add_tag_new_tag(
    sample_tag: Tag, tag_repository: SATagRepository, session: AsyncSession
):
    tag_id = await tag_repository.get_or_add_tag(session, sample_tag)

    assert tag_id is not None
    assert isinstance(tag_id, int)
    assert tag_id > 0


@pytest.mark.asyncio
async def test_get_or_add_tag_existing_tag(
    sample_tag: Tag, tag_repository: SATagRepository, session: AsyncSession
):
    first_id = await tag_repository.get_or_add_tag(session, sample_tag)
    second_id = await tag_repository.get_or_add_tag(session, sample_tag)

    assert first_id == second_id


@pytest.mark.asyncio
async def test_get_all_tags_with_data(
    sample_tag: Tag,
    sample_tag_male: Tag,
    sample_tag_female: Tag,
    tag_repository: SATagRepository,
    session: AsyncSession,
):

    await tag_repository.get_or_add_tag(session, sample_tag)
    await tag_repository.get_or_add_tag(session, sample_tag_female)
    await tag_repository.get_or_add_tag(session, sample_tag_male)

    tags = await tag_repository.get_all_tags()

    assert len(tags) == 3
    assert ("digital", False, False) in tags
    assert ("shota", True, False) in tags
    assert ("loli", False, True) in tags
