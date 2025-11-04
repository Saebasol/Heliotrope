from unittest.mock import AsyncMock

import pytest
from yggdrasil.application.usecases.create.info import CreateInfoUseCase
from yggdrasil.domain.entities.info import Info

from tests.unit.domain.entities.conftest import sample_info as sample_info


@pytest.mark.asyncio
async def test_create_info(
    mock_repository: AsyncMock,
    sample_info: Info,
):
    usecase = CreateInfoUseCase(info_repository=mock_repository)

    await usecase.execute(sample_info)

    mock_repository.add_info.assert_awaited_once_with(sample_info)
