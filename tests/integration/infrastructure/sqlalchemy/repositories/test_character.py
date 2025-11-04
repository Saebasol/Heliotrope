from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from yggdrasil.domain.entities.character import Character
from yggdrasil.infrastructure.sqlalchemy.entities.character import CharacterSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.character import (
    SACharacterRepository,
)

from tests.unit.domain.entities.conftest import sample_character as sample_character


@pytest.mark.asyncio
async def test_get_or_add_character_new_character(
    sample_character: Character,
    character_repository: SACharacterRepository,
    session: AsyncSession,
):
    character = await character_repository.get_or_add_character(
        session, sample_character
    )

    assert character is not None
    assert isinstance(character, CharacterSchema)


@pytest.mark.asyncio
async def test_get_or_add_character_existing_character(
    sample_character: Character,
    character_repository: SACharacterRepository,
    session: AsyncSession,
):
    first = await character_repository.get_or_add_character(session, sample_character)
    second = await character_repository.get_or_add_character(session, sample_character)
    await session.commit()

    assert first == second


@pytest.mark.asyncio
async def test_get_all_characters_with_data(
    sample_character: Character,
    character_repository: SACharacterRepository,
    session: AsyncSession,
):
    character1 = sample_character
    character1.character = "character_one"
    character1.url = "/character/one.html"
    character2 = deepcopy(sample_character)
    character2.character = "character_two"
    character2.url = "/character/two.html"
    character3 = deepcopy(sample_character)
    character3.character = "character_three"
    character3.url = "/character/three.html"

    await character_repository.get_or_add_character(session, character1)
    await character_repository.get_or_add_character(session, character2)
    await character_repository.get_or_add_character(session, character3)

    await session.commit()

    characters = await character_repository.get_all_characters()

    assert len(characters) == 3
    assert "character_one" in characters
    assert "character_two" in characters
    assert "character_three" in characters
