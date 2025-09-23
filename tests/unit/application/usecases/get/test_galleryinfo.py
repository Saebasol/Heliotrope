from unittest.mock import AsyncMock

import pytest

from heliotrope.application.usecases.get.galleryinfo import (
    GetAllGalleryinfoIdsUseCase,
    GetGalleryinfoUseCase,
)
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.exceptions import GalleryinfoNotFound
from tests.unit.domain.entities.conftest import *


@pytest.fixture
def get_usecase(mock_repository: AsyncMock):
    return GetGalleryinfoUseCase(galleryinfo_repository=mock_repository)


@pytest.fixture()
def get_all_ids_usecase(mock_repository: AsyncMock):
    return GetAllGalleryinfoIdsUseCase(galleryinfo_repository=mock_repository)


@pytest.mark.asyncio
async def test_get_galleryinfo(
    get_usecase: GetGalleryinfoUseCase,
    mock_repository: AsyncMock,
    sample_galleryinfo: Galleryinfo,
):
    mock_repository.get_galleryinfo.return_value = sample_galleryinfo

    result = await get_usecase.execute(sample_galleryinfo.id)

    assert result == sample_galleryinfo
    mock_repository.get_galleryinfo.assert_awaited_once_with(sample_galleryinfo.id)


@pytest.mark.asyncio
async def test_get_nonexistent_galleryinfo(
    get_usecase: GetGalleryinfoUseCase,
    mock_repository: AsyncMock,
    sample_galleryinfo: Galleryinfo,
):
    mock_repository.get_galleryinfo.return_value = None

    with pytest.raises(GalleryinfoNotFound) as exc_info:
        await get_usecase.execute(sample_galleryinfo.id)

    assert str(sample_galleryinfo.id) in str(exc_info.value)
    mock_repository.get_galleryinfo.assert_awaited_once_with(sample_galleryinfo.id)


@pytest.mark.asyncio
async def test_get_all_galleryinfo_ids(
    get_all_ids_usecase: GetAllGalleryinfoIdsUseCase,
    mock_repository: AsyncMock,
):
    mock_repository.get_all_galleryinfo_ids.return_value = [1, 2, 3]

    result = await get_all_ids_usecase.execute()

    assert result == [1, 2, 3]
    mock_repository.get_all_galleryinfo_ids.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_galleryinfo_ids_with_await_syntax(
    get_all_ids_usecase: GetAllGalleryinfoIdsUseCase,
    mock_repository: AsyncMock,
):
    mock_repository.get_all_galleryinfo_ids.return_value = [1, 2, 3]

    result = await get_all_ids_usecase

    assert result == [1, 2, 3]
    mock_repository.get_all_galleryinfo_ids.assert_awaited_once()
