from unittest.mock import AsyncMock, MagicMock

import pytest

from heliotrope.application.dtos.thumbnail import Size
from heliotrope.application.usecases.get.resolved_image import (
    GetResolvedImageUseCase,
    GetResolvedThumbnailUseCase,
)
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.resolved_image import ResolvedImage
from tests.unit.domain.entities.conftest import sample_file as sample_file
from tests.unit.domain.entities.conftest import (
    sample_resolved_image as sample_resolved_image,
)


@pytest.fixture
def mock_resolved_image_repository():
    return MagicMock()


def test_get_resolved_image_usecase_execute(
    mock_resolved_image_repository: MagicMock,
    sample_file: File,
    sample_resolved_image: ResolvedImage,
):
    usecase = GetResolvedImageUseCase(
        resolved_image_repository=mock_resolved_image_repository
    )
    galleryinfo_id = 1

    mock_resolved_image_repository.resolve_image.return_value = sample_resolved_image

    result = usecase.execute(galleryinfo_id, sample_file)

    mock_resolved_image_repository.resolve_image.assert_called_once_with(
        galleryinfo_id, sample_file
    )
    assert result == sample_resolved_image


def test_get_resolved_thumbnail_usecase_execute(
    mock_resolved_image_repository: MagicMock,
    sample_file: File,
    sample_resolved_image: ResolvedImage,
):
    usecase = GetResolvedThumbnailUseCase(
        resolved_image_repository=mock_resolved_image_repository
    )
    galleryinfo_id = 1
    size = Size.SMALL

    mock_resolved_image_repository.resolve_thumbnail.return_value = (
        sample_resolved_image
    )

    result = usecase.execute(galleryinfo_id, sample_file, size)

    mock_resolved_image_repository.resolve_thumbnail.assert_called_once_with(
        galleryinfo_id, sample_file, size
    )
    assert result == sample_resolved_image
