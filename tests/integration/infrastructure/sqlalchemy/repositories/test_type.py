from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.type import Type
from heliotrope.infrastructure.sqlalchemy.repositories.type import SATypeRepository
from tests.unit.domain.entities.conftest import sample_type as sample_type


@pytest.mark.asyncio
async def test_get_or_add_type_new_type(
    sample_type: Type, type_repository: SATypeRepository, session: AsyncSession
):
    type_id = await type_repository.get_or_add_type(session, sample_type)

    assert type_id is not None
    assert isinstance(type_id, int)
    assert type_id > 0


@pytest.mark.asyncio
async def test_get_or_add_type_existing_type(
    sample_type: Type, type_repository: SATypeRepository, session: AsyncSession
):
    first_id = await type_repository.get_or_add_type(session, sample_type)
    second_id = await type_repository.get_or_add_type(session, sample_type)

    assert first_id == second_id


@pytest.mark.asyncio
async def test_get_all_types_with_data(
    sample_type: Type,
    type_repository: SATypeRepository,
    session: AsyncSession,
):
    sample_type.type = "type"
    type2 = deepcopy(sample_type)
    type2.type = "type_two"
    type3 = deepcopy(sample_type)
    type3.type = "type_three"

    await type_repository.get_or_add_type(session, sample_type)
    await type_repository.get_or_add_type(session, type2)
    await type_repository.get_or_add_type(session, type3)

    types = await type_repository.get_all_types()

    assert len(types) == 3
    assert "type" in types
    assert "type_two" in types
    assert "type_three" in types
