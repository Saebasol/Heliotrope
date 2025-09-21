from unittest.mock import AsyncMock

import pytest

from heliotrope.application.usecases.create.galleryinfo import CreateGalleryinfoUseCase
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from tests.unit.domain.entities.conftest import *


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.mark.asyncio
async def test_create_galleryinfo_usecase(
    mock_repository: AsyncMock, sample_galleryinfo: Galleryinfo
):
    mock_repository.add_galleryinfo.return_value = None

    usecase = CreateGalleryinfoUseCase(galleryinfo_repository=mock_repository)
    # When
    await usecase.execute(sample_galleryinfo)

    # Then
    mock_repository.add_galleryinfo.assert_awaited_once_with(sample_galleryinfo)
