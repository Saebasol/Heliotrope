from copy import deepcopy

import pytest

from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)
from tests.unit.domain.entities.conftest import sample_galleryinfo as sample_galleryinfo


@pytest.mark.asyncio
async def test_add_galleryinfo_new_galleryinfo(
    sample_galleryinfo: Galleryinfo, galleryinfo_repository: SAGalleryinfoRepository
):
    galleryinfo_id = await galleryinfo_repository.add_galleryinfo(sample_galleryinfo)

    assert galleryinfo_id is not None
    assert isinstance(galleryinfo_id, int)
    assert galleryinfo_id == sample_galleryinfo.id


@pytest.mark.asyncio
async def test_get_galleryinfo_existing(
    sample_galleryinfo: Galleryinfo, galleryinfo_repository: SAGalleryinfoRepository
):
    await galleryinfo_repository.add_galleryinfo(sample_galleryinfo)

    retrieved_galleryinfo = await galleryinfo_repository.get_galleryinfo(
        sample_galleryinfo.id
    )

    assert retrieved_galleryinfo is not None
    assert retrieved_galleryinfo.id == sample_galleryinfo.id
    assert retrieved_galleryinfo.title == sample_galleryinfo.title
    assert retrieved_galleryinfo.japanese_title == sample_galleryinfo.japanese_title
    assert retrieved_galleryinfo.galleryurl == sample_galleryinfo.galleryurl


@pytest.mark.asyncio
async def test_get_galleryinfo_non_existing(
    galleryinfo_repository: SAGalleryinfoRepository,
):
    non_existing_id = 999999

    retrieved_galleryinfo = await galleryinfo_repository.get_galleryinfo(
        non_existing_id
    )

    assert retrieved_galleryinfo is None


@pytest.mark.asyncio
async def test_is_galleryinfo_exists_true(
    sample_galleryinfo: Galleryinfo, galleryinfo_repository: SAGalleryinfoRepository
):
    await galleryinfo_repository.add_galleryinfo(sample_galleryinfo)

    exists = await galleryinfo_repository.is_galleryinfo_exists(sample_galleryinfo.id)

    assert exists is True


@pytest.mark.asyncio
async def test_is_galleryinfo_exists_false(
    galleryinfo_repository: SAGalleryinfoRepository,
):
    non_existing_id = 999999

    exists = await galleryinfo_repository.is_galleryinfo_exists(non_existing_id)

    assert exists is False


@pytest.mark.asyncio
async def test_get_all_galleryinfo_ids_with_data(
    sample_galleryinfo: Galleryinfo, galleryinfo_repository: SAGalleryinfoRepository
):
    galleryinfo1 = sample_galleryinfo
    galleryinfo2 = deepcopy(sample_galleryinfo)
    galleryinfo2.id = 2639955
    galleryinfo2.title = "Another Title"
    galleryinfo3 = deepcopy(sample_galleryinfo)
    galleryinfo3.id = 2639956
    galleryinfo3.title = "Third Title"

    await galleryinfo_repository.add_galleryinfo(galleryinfo1)
    await galleryinfo_repository.add_galleryinfo(galleryinfo2)
    await galleryinfo_repository.add_galleryinfo(galleryinfo3)

    galleryinfo_ids = await galleryinfo_repository.get_all_galleryinfo_ids()

    assert len(galleryinfo_ids) == 3
    assert sample_galleryinfo.id in galleryinfo_ids
    assert 2639955 in galleryinfo_ids
    assert 2639956 in galleryinfo_ids
    # IDs should be ordered
    assert galleryinfo_ids == sorted(galleryinfo_ids)


@pytest.mark.asyncio
async def test_delete_galleryinfo_existing(
    sample_galleryinfo: Galleryinfo, galleryinfo_repository: SAGalleryinfoRepository
):
    await galleryinfo_repository.add_galleryinfo(sample_galleryinfo)

    # Verify it exists before deletion
    exists_before = await galleryinfo_repository.is_galleryinfo_exists(
        sample_galleryinfo.id
    )
    assert exists_before is True

    await galleryinfo_repository.delete_galleryinfo(sample_galleryinfo.id)

    # Verify it doesn't exist after deletion
    exists_after = await galleryinfo_repository.is_galleryinfo_exists(
        sample_galleryinfo.id
    )
    assert exists_after is False


@pytest.mark.asyncio
async def test_delete_galleryinfo_non_existing(
    galleryinfo_repository: SAGalleryinfoRepository,
):
    non_existing_id = 999999

    # Should not raise an error when deleting non-existing galleryinfo
    await galleryinfo_repository.delete_galleryinfo(non_existing_id)

    # Verify it still doesn't exist
    exists = await galleryinfo_repository.is_galleryinfo_exists(non_existing_id)
    assert exists is False
