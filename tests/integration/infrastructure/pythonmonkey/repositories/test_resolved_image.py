import pytest
import pytest_asyncio

from heliotrope.application.dtos.thumbnail import Size
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.resolved_image import ResolvedImage
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.pythonmonkey import JavaScriptInterpreter
from heliotrope.infrastructure.pythonmonkey.repositories.resolved_image import (
    PythonMonkeyResolvedImageRepository,
)


@pytest_asyncio.fixture
async def repository(hitomi_la: HitomiLa):
    js_interpreter = await JavaScriptInterpreter.setup(hitomi_la)
    return PythonMonkeyResolvedImageRepository(js_interpreter)


@pytest.fixture
def test_file_avif():
    return File.from_dict(
        {
            "hasavif": True,
            "hash": "4c519d488b39e33aa503ac650084eb03c4b61e64778c488cdec0462f378f83d3",
            "height": 1821,
            "name": "01.jpg",
            "width": 1290,
            "hasjxl": False,
            "haswebp": True,
            "single": False,
        }
    )


@pytest.fixture
def test_file_webp():
    return File.from_dict(
        {
            "hasavif": False,
            "hash": "4c519d488b39e33aa503ac650084eb03c4b61e64778c488cdec0462f378f83d3",
            "height": 1821,
            "name": "01.jpg",
            "width": 1290,
            "hasjxl": False,
            "haswebp": True,
            "single": False,
        }
    )


@pytest.mark.asyncio
async def test_repository_initialization(
    repository: PythonMonkeyResolvedImageRepository,
):
    assert repository.javascript_interpreter is not None
    assert repository._thumbnail_resolver is not None


@pytest.mark.asyncio
async def test_resolve_image(
    repository: PythonMonkeyResolvedImageRepository, test_file_avif: File
):
    result = repository.resolve_image(2033723, test_file_avif)

    assert isinstance(result, ResolvedImage)
    assert result.file == test_file_avif
    assert isinstance(result.url, str)
    assert len(result.url) > 0


@pytest.mark.asyncio
async def test_resolve_thumbnails_all_sizes_avif(
    repository: PythonMonkeyResolvedImageRepository, test_file_avif: File
):
    """Test thumbnail resolution for all sizes with AVIF."""
    sizes = [Size.SMALLSMALL, Size.SMALL, Size.SMALLBIG, Size.BIG]

    for size in sizes:
        result = repository.resolve_thumbnail(2033723, test_file_avif, size)

        assert isinstance(result, ResolvedImage)
        assert result.file == test_file_avif
        assert isinstance(result.url, str)
        assert len(result.url) > 0


@pytest.mark.asyncio
async def test_resolve_thumbnails_all_sizes_webp(
    repository: PythonMonkeyResolvedImageRepository, test_file_webp: File
):
    sizes = [Size.SMALLSMALL, Size.SMALL, Size.SMALLBIG, Size.BIG]

    for size in sizes:
        result = repository.resolve_thumbnail(2033723, test_file_webp, size)

        assert isinstance(result, ResolvedImage)
        assert result.file == test_file_webp
        assert isinstance(result.url, str)
        assert len(result.url) > 0


@pytest.mark.asyncio
async def test_thumbnail_format_selection(
    repository: PythonMonkeyResolvedImageRepository,
    test_file_avif: File,
    test_file_webp: File,
):
    # Test with AVIF support
    avif_result = repository.resolve_thumbnail(2033723, test_file_avif, Size.SMALL)

    # Test with WebP only
    webp_result = repository.resolve_thumbnail(2033723, test_file_webp, Size.SMALL)

    # URLs should be different (AVIF vs WebP paths)
    assert avif_result.url != webp_result.url


@pytest.mark.asyncio
async def test_integration_with_real_urls(
    repository: PythonMonkeyResolvedImageRepository,
    test_file_avif: File,
    hitomi_la: HitomiLa,
):
    # Test image URL
    image_result = repository.resolve_image(2033723, test_file_avif)
    image_response = await hitomi_la.session.request(
        "GET", image_result.url, headers=hitomi_la.headers
    )
    assert image_response.status == 200

    # Test thumbnail URLs
    sizes = [Size.SMALLSMALL, Size.SMALL, Size.SMALLBIG, Size.BIG]
    for size in sizes:
        thumbnail_result = repository.resolve_thumbnail(2033723, test_file_avif, size)
        thumbnail_response = await hitomi_la.session.request(
            "GET", thumbnail_result.url, headers=hitomi_la.headers
        )
        assert thumbnail_response.status == 200
