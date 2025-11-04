from unittest.mock import AsyncMock

import pytest
from yggdrasil.application.usecases.delete.galleryinfo import DeleteGalleryinfoUseCase
from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.domain.exceptions import GalleryinfoNotFound

from tests.unit.domain.entities.conftest import *


@pytest.fixture
def usecase(mock_repository: AsyncMock):
    return DeleteGalleryinfoUseCase(galleryinfo_repository=mock_repository)


@pytest.mark.asyncio
async def test_delete_existing_galleryinfo(
    usecase: DeleteGalleryinfoUseCase,
    mock_repository: AsyncMock,
    sample_galleryinfo: Galleryinfo,
):
    mock_repository.is_galleryinfo_exists.return_value = True

    await usecase.execute(sample_galleryinfo.id)

    mock_repository.is_galleryinfo_exists.assert_awaited_once_with(
        sample_galleryinfo.id
    )
    mock_repository.delete_galleryinfo.assert_awaited_once_with(sample_galleryinfo.id)


@pytest.mark.asyncio
async def test_delete_nonexistent_galleryinfo(
    usecase: DeleteGalleryinfoUseCase,
    mock_repository: AsyncMock,
    sample_galleryinfo: Galleryinfo,
):
    mock_repository.is_galleryinfo_exists.return_value = False

    with pytest.raises(GalleryinfoNotFound) as exc_info:
        await usecase.execute(sample_galleryinfo.id)

    assert str(sample_galleryinfo.id) in str(exc_info.value)

    mock_repository.is_galleryinfo_exists.assert_awaited_once_with(
        sample_galleryinfo.id
    )
    mock_repository.delete_galleryinfo.assert_not_awaited()
