from unittest.mock import AsyncMock

import pytest

from heliotrope.application.usecases.get.info import (
    GetAllInfoIdsUseCase,
    GetInfoUseCase,
    GetListInfoUseCase,
    GetRandomInfoUseCase,
    SearchByQueryUseCase,
)
from heliotrope.domain.entities.info import Info
from heliotrope.domain.exceptions import InfoNotFound
from tests.unit.domain.entities.conftest import sample_info as sample_info


@pytest.fixture
def get_info_usecase(mock_repository: AsyncMock):
    return GetInfoUseCase(info_repository=mock_repository)


@pytest.fixture
def get_all_info_ids_usecase(mock_repository: AsyncMock):
    return GetAllInfoIdsUseCase(info_repository=mock_repository)


@pytest.fixture
def get_random_info_usecase(mock_repository: AsyncMock):
    return GetRandomInfoUseCase(info_repository=mock_repository)


@pytest.mark.asyncio
async def test_get_info(
    get_info_usecase: GetInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.get_info.return_value = sample_info

    result = await get_info_usecase.execute(sample_info.id)

    assert result == sample_info
    mock_repository.get_info.assert_awaited_once_with(sample_info.id)


@pytest.mark.asyncio
async def test_get_nonexistent_info(
    get_info_usecase: GetInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.get_info.return_value = None

    with pytest.raises(InfoNotFound) as exc_info:
        await get_info_usecase.execute(sample_info.id)

    assert str(sample_info.id) in str(exc_info.value)
    mock_repository.get_info.assert_awaited_once_with(sample_info.id)


@pytest.mark.asyncio
async def test_get_list_info(
    mock_repository: AsyncMock,
    sample_info: Info,
):
    usecase = GetListInfoUseCase(info_repository=mock_repository)
    mock_repository.get_list_info.return_value = [sample_info]

    result = await usecase.execute(page=1, item=10)

    assert result == [sample_info]
    mock_repository.get_list_info.assert_awaited_once_with(1, 10)


@pytest.mark.asyncio
async def test_get_all_info_ids(
    get_all_info_ids_usecase: GetAllInfoIdsUseCase,
    mock_repository: AsyncMock,
):
    mock_repository.get_all_info_ids.return_value = [1, 2, 3]

    result = await get_all_info_ids_usecase.execute()

    assert result == [1, 2, 3]
    mock_repository.get_all_info_ids.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_info_ids_with_await_syntax(
    get_all_info_ids_usecase: GetAllInfoIdsUseCase,
    mock_repository: AsyncMock,
):
    mock_repository.get_all_info_ids.return_value = [1, 2, 3]

    result = await get_all_info_ids_usecase

    assert result == [1, 2, 3]

    assert result == [1, 2, 3]
    mock_repository.get_all_info_ids.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_random_info(
    get_random_info_usecase: GetRandomInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.get_random_info.return_value = sample_info

    query = ["tag1", "tag2"]
    result = await get_random_info_usecase.execute(query)

    assert result == sample_info
    mock_repository.get_random_info.assert_awaited_once_with(query)


@pytest.mark.asyncio
async def test_get_random_info_not_found(
    get_random_info_usecase: GetRandomInfoUseCase,
    mock_repository: AsyncMock,
):
    mock_repository.get_random_info.return_value = None

    query = ["tag1", "tag2"]
    with pytest.raises(InfoNotFound) as exc_info:
        await get_random_info_usecase.execute(query)

    assert all(tag in str(exc_info.value) for tag in query)
    mock_repository.get_random_info.assert_awaited_once_with(query)


@pytest.mark.asyncio
async def test_search_by_query(
    mock_repository: AsyncMock,
    sample_info: Info,
):
    usecase = SearchByQueryUseCase(info_repository=mock_repository)
    mock_repository.search_by_query.return_value = (1, [sample_info])

    query = ["tag1", "tag2"]
    result = await usecase.execute(query, page=0, item=10)

    assert result == (1, [sample_info])
    mock_repository.search_by_query.assert_awaited_once_with(query, 0, 10)
