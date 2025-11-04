# pyright: reportPrivateUsage=false
import pytest
from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.infrastructure.hitomila import HitomiLa
from yggdrasil.infrastructure.hitomila.repositories.galleryinfo import (
    HitomiLaGalleryinfoRepository,
)

from tests.unit.domain.entities.conftest import *


@pytest.fixture
def repository(hitomi_la: HitomiLa):
    return HitomiLaGalleryinfoRepository(hitomi_la)


@pytest.mark.asyncio
async def test_get_galleryinfo_exists(repository: HitomiLaGalleryinfoRepository):
    test_id = 1

    result = await repository.get_galleryinfo(test_id)

    assert isinstance(result, Galleryinfo)
    assert result.title is not None
    assert len(result.title) > 0


@pytest.mark.asyncio
async def test_get_galleryinfo_not_exists(repository: HitomiLaGalleryinfoRepository):
    invalid_id = 99999999

    result = await repository.get_galleryinfo(invalid_id)

    assert result is None


@pytest.mark.asyncio
async def test_is_galleryinfo_exists_true(repository: HitomiLaGalleryinfoRepository):
    test_id = 1

    exists = await repository.is_galleryinfo_exists(test_id)

    assert isinstance(exists, bool)


@pytest.mark.asyncio
async def test_is_galleryinfo_exists_false(repository: HitomiLaGalleryinfoRepository):
    invalid_id = 99999999

    exists = await repository.is_galleryinfo_exists(invalid_id)

    assert exists is False


@pytest.mark.asyncio
async def test_get_galleryinfo_ids_with_pagination(
    repository: HitomiLaGalleryinfoRepository,
):
    page = 1
    item_count = 10

    ids = await repository.get_galleryinfo_ids(page=page, item=item_count)

    assert isinstance(ids, list)
    assert len(ids) <= item_count
    for gallery_id in ids:
        assert isinstance(gallery_id, int)
        assert gallery_id > 0


@pytest.mark.asyncio
async def test_get_galleryinfo_ids_different_pages(
    repository: HitomiLaGalleryinfoRepository,
):
    page1_ids = await repository.get_galleryinfo_ids(page=1, item=5)
    page2_ids = await repository.get_galleryinfo_ids(page=2, item=5)

    assert isinstance(page1_ids, list)
    assert isinstance(page2_ids, list)

    if len(page1_ids) > 0 and len(page2_ids) > 0:
        assert page1_ids != page2_ids


@pytest.mark.asyncio
async def test_get_all_galleryinfo_ids(repository: HitomiLaGalleryinfoRepository):
    all_ids = await repository.get_all_galleryinfo_ids()

    assert isinstance(all_ids, list)
    assert len(all_ids) > 0

    for gallery_id in all_ids[:10]:
        assert isinstance(gallery_id, int)
        assert gallery_id > 0


@pytest.mark.asyncio
async def test_get_galleryinfo_structure(repository: HitomiLaGalleryinfoRepository):
    test_id = 1

    galleryinfo = await repository.get_galleryinfo(test_id)

    assert hasattr(galleryinfo, "id")
    assert hasattr(galleryinfo, "title")
    assert hasattr(galleryinfo, "type")

    assert galleryinfo is not None
    assert isinstance(galleryinfo.id, int)
    assert isinstance(galleryinfo.title, str)


@pytest.mark.asyncio
async def test_add_galleryinfo_not_implemented(
    repository: HitomiLaGalleryinfoRepository, sample_galleryinfo: Galleryinfo
):
    with pytest.raises(NotImplementedError):
        await repository.add_galleryinfo(sample_galleryinfo)


@pytest.mark.asyncio
async def test_delete_galleryinfo_not_implemented(
    repository: HitomiLaGalleryinfoRepository,
):
    with pytest.raises(NotImplementedError):
        await repository.delete_galleryinfo(123456)


@pytest.mark.asyncio
async def test_request_error_handling(repository: HitomiLaGalleryinfoRepository):
    invalid_id = 999999999999

    result = await repository.get_galleryinfo(invalid_id)

    assert result is None


@pytest.mark.asyncio
async def test_multiple_concurrent_requests(repository: HitomiLaGalleryinfoRepository):
    import asyncio

    test_ids = [1000000, 1000001, 1000002]

    tasks = [repository.get_galleryinfo(id) for id in test_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    assert len(results) == len(test_ids)

    for result in results:
        assert not isinstance(result, Exception)
