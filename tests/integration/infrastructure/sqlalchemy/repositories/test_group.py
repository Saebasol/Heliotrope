from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.group import Group
from heliotrope.infrastructure.sqlalchemy.repositories.group import SAGroupRepository
from tests.unit.domain.entities.conftest import sample_group as sample_group


@pytest.mark.asyncio
async def test_get_or_add_group_new_group(
    sample_group: Group, group_repository: SAGroupRepository, session: AsyncSession
):
    group_id = await group_repository.get_or_add_group(session, sample_group)

    assert group_id is not None
    assert isinstance(group_id, int)
    assert group_id > 0


@pytest.mark.asyncio
async def test_get_or_add_group_existing_group(
    sample_group: Group, group_repository: SAGroupRepository, session: AsyncSession
):
    first_id = await group_repository.get_or_add_group(session, sample_group)
    second_id = await group_repository.get_or_add_group(session, sample_group)

    assert first_id == second_id


@pytest.mark.asyncio
async def test_get_all_groups_with_data(
    sample_group: Group, group_repository: SAGroupRepository, session: AsyncSession
):
    group1 = sample_group
    group1.group = "group_one"
    group1.url = "/group/one.html"
    group2 = deepcopy(sample_group)
    group2.group = "group_two"
    group2.url = "/group/two.html"
    group3 = deepcopy(sample_group)
    group3.group = "group_three"
    group3.url = "/group/three.html"

    await group_repository.get_or_add_group(session, group1)
    await group_repository.get_or_add_group(session, group2)
    await group_repository.get_or_add_group(session, group3)

    groups = await group_repository.get_all_groups()

    assert len(groups) == 3
    assert "group_one" in groups
    assert "group_two" in groups
    assert "group_three" in groups
