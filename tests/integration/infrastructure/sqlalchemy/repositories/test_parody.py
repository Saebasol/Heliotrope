from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from heliotrope.domain.entities.parody import Parody
from heliotrope.infrastructure.sqlalchemy.entities.parody import ParodySchema
from heliotrope.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from tests.unit.domain.entities.conftest import sample_artist as sample_artist


@pytest.mark.asyncio
async def test_get_or_add_parody_new_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    parody = await parody_repository.get_or_add_parody(session, sample_parody)

    assert parody is not None
    assert isinstance(parody, ParodySchema)


@pytest.mark.asyncio
async def test_get_or_add_parody_existing_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    first = await parody_repository.get_or_add_parody(session, sample_parody)
    second = await parody_repository.get_or_add_parody(session, sample_parody)

    await session.commit()

    assert first == second


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

    await session.commit()

    parodies = await parody_repository.get_all_parodies()

    assert len(parodies) == 3
    assert "parody_one" in parodies
    assert "parody_two" in parodies
    assert "parody_three" in parodies
