from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.parody import Parody
from heliotrope.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from tests.unit.domain.entities.conftest import sample_artist as sample_artist


@pytest.mark.asyncio
async def test_get_or_add_parody_new_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    parody_id = await parody_repository.get_or_add_parody(session, sample_parody)

    assert parody_id is not None
    assert isinstance(parody_id, int)
    assert parody_id > 0


@pytest.mark.asyncio
async def test_get_or_add_parody_existing_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    first_id = await parody_repository.get_or_add_parody(session, sample_parody)
    second_id = await parody_repository.get_or_add_parody(session, sample_parody)

    assert first_id == second_id


@pytest.mark.asyncio
async def test_get_all_parodies_with_data(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    parody1 = sample_parody
    parody1.parody = "parody_one"
    parody1.url = "/parody/one.html"
    parody2 = deepcopy(sample_parody)
    parody2.parody = "parody_two"
    parody2.url = "/parody/two.html"
    parody3 = deepcopy(sample_parody)
    parody3.parody = "parody_three"
    parody3.url = "/parody/three.html"

    await parody_repository.get_or_add_parody(session, parody1)
    await parody_repository.get_or_add_parody(session, parody2)
    await parody_repository.get_or_add_parody(session, parody3)
    parodies = await parody_repository.get_all_parodies()

    assert len(parodies) == 3
    assert "parody_one" in parodies
    assert "parody_two" in parodies
    assert "parody_three" in parodies
