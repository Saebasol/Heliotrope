from unittest.mock import AsyncMock

import pytest

from heliotrope.application.usecases.get.info import GetInfoUseCase
from heliotrope.domain.entities.info import Info
from heliotrope.domain.exceptions import InfoNotFound
from tests.unit.domain.entities.conftest import sample_info as sample_info


@pytest.fixture
def usecase(mock_repository: AsyncMock):
    return GetInfoUseCase(info_repository=mock_repository)


@pytest.mark.asyncio
async def test_get_info(
    usecase: GetInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.get_info.return_value = sample_info

    result = await usecase.execute(sample_info.id)

    assert result == sample_info
    mock_repository.get_info.assert_awaited_once_with(sample_info.id)


@pytest.mark.asyncio
async def test_get_nonexistent_info(
    usecase: GetInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.get_info.return_value = None

    with pytest.raises(InfoNotFound) as exc_info:
        await usecase.execute(sample_info.id)

    assert str(sample_info.id) in str(exc_info.value)
    mock_repository.get_info.assert_awaited_once_with(sample_info.id)
