from unittest.mock import AsyncMock

import pytest
from yggdrasil.application.usecases.get.all_tags import GetAllTagsUseCase
from yggdrasil.domain.entities.all_tags import AllTags


@pytest.fixture
def mock_artist_repository():
    return AsyncMock()


@pytest.fixture
def mock_character_repository():
    return AsyncMock()


@pytest.fixture
def mock_group_repository():
    return AsyncMock()


@pytest.fixture
def mock_language_info_repository():
    return AsyncMock()


@pytest.fixture
def mock_parody_repository():
    return AsyncMock()


@pytest.fixture
def mock_tag_repository():
    return AsyncMock()


@pytest.fixture
def mock_type_repository():
    return AsyncMock()


@pytest.fixture
def usecase(
    mock_artist_repository: AsyncMock,
    mock_character_repository: AsyncMock,
    mock_group_repository: AsyncMock,
    mock_language_info_repository: AsyncMock,
    mock_parody_repository: AsyncMock,
    mock_tag_repository: AsyncMock,
    mock_type_repository: AsyncMock,
):
    return GetAllTagsUseCase(
        artist_repository=mock_artist_repository,
        character_repository=mock_character_repository,
        group_repository=mock_group_repository,
        language_info_repository=mock_language_info_repository,
        parody_repository=mock_parody_repository,
        tag_repository=mock_tag_repository,
        type_repository=mock_type_repository,
    )


@pytest.mark.asyncio
async def test_get_all_tags(
    usecase: GetAllTagsUseCase,
    mock_artist_repository: AsyncMock,
    mock_character_repository: AsyncMock,
    mock_group_repository: AsyncMock,
    mock_language_info_repository: AsyncMock,
    mock_parody_repository: AsyncMock,
    mock_tag_repository: AsyncMock,
    mock_type_repository: AsyncMock,
):
    # Arrange
    mock_artist_repository.get_all_artists.return_value = ["artist one", "artist two"]
    mock_character_repository.get_all_characters.return_value = [
        "character one",
        "character two",
    ]
    mock_group_repository.get_all_groups.return_value = ["group one", "group two"]
    mock_language_info_repository.get_all_language_infos.return_value = [
        "korean",
        "english",
    ]
    mock_parody_repository.get_all_parodies.return_value = ["parody one", "parody two"]
    mock_tag_repository.get_all_tags.return_value = [
        ("normal tag", False, False),  # normal tag
        ("male tag", True, False),  # male tag
        ("female tag", False, True),  # female tag
        ("both tag", True, True),  # both (should be ignored)
    ]
    mock_type_repository.get_all_types.return_value = ["type one", "type two"]

    result = await usecase.execute()

    expected = AllTags(
        artists=["artist_one", "artist_two"],
        characters=["character_one", "character_two"],
        groups=["group_one", "group_two"],
        language=["korean", "english"],
        series=["parody_one", "parody_two"],
        tag=["normal_tag"],
        female=["female_tag"],
        male=["male_tag"],
        type=["type_one", "type_two"],
    )

    assert result == expected

    # Verify all repositories were called
    mock_artist_repository.get_all_artists.assert_awaited_once()
    mock_character_repository.get_all_characters.assert_awaited_once()
    mock_group_repository.get_all_groups.assert_awaited_once()
    mock_language_info_repository.get_all_language_infos.assert_awaited_once()
    mock_parody_repository.get_all_parodies.assert_awaited_once()
    mock_tag_repository.get_all_tags.assert_awaited_once()
    mock_type_repository.get_all_types.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_tags_with_await_syntax(
    usecase: GetAllTagsUseCase,
    mock_artist_repository: AsyncMock,
    mock_character_repository: AsyncMock,
    mock_group_repository: AsyncMock,
    mock_language_info_repository: AsyncMock,
    mock_parody_repository: AsyncMock,
    mock_tag_repository: AsyncMock,
    mock_type_repository: AsyncMock,
):
    mock_artist_repository.get_all_artists.return_value = ["test artist"]
    mock_character_repository.get_all_characters.return_value = ["test character"]
    mock_group_repository.get_all_groups.return_value = ["test group"]
    mock_language_info_repository.get_all_language_infos.return_value = [
        "test language"
    ]
    mock_parody_repository.get_all_parodies.return_value = ["test parody"]
    mock_tag_repository.get_all_tags.return_value = [("test tag", False, False)]
    mock_type_repository.get_all_types.return_value = ["test type"]

    result = await usecase

    expected = AllTags(
        artists=["test_artist"],
        characters=["test_character"],
        groups=["test_group"],
        language=["test_language"],
        series=["test_parody"],
        tag=["test_tag"],
        female=[],
        male=[],
        type=["test_type"],
    )

    assert result == expected
