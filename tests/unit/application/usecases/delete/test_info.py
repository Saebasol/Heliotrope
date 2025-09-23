from unittest.mock import AsyncMock

import pytest

from heliotrope.application.usecases.delete.info import DeleteInfoUseCase
from heliotrope.domain.entities.info import Info
from heliotrope.domain.exceptions import InfoNotFound
from tests.unit.domain.entities.conftest import sample_info as sample_info


@pytest.fixture
def usecase(mock_repository: AsyncMock):
    return DeleteInfoUseCase(info_repository=mock_repository)


@pytest.mark.asyncio
async def test_delete_existing_info(
    usecase: DeleteInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.is_info_exists.return_value = True

    await usecase.execute(sample_info.id)

    mock_repository.is_info_exists.assert_awaited_once_with(sample_info.id)
    mock_repository.delete_info.assert_awaited_once_with(sample_info.id)


@pytest.mark.asyncio
async def test_delete_nonexistent_info(
    usecase: DeleteInfoUseCase,
    mock_repository: AsyncMock,
    sample_info: Info,
):
    mock_repository.is_info_exists.return_value = False

    with pytest.raises(InfoNotFound) as exc_info:
        await usecase.execute(sample_info.id)

    assert str(sample_info.id) in str(exc_info.value)

    mock_repository.is_info_exists.assert_awaited_once_with(sample_info.id)
    mock_repository.delete_info.assert_not_awaited()
