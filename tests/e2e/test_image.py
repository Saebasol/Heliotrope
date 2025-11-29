import httpx
import pytest
import pytest_asyncio
from yggdrasil.domain.entities.resolved_image import ResolvedImage
from yggdrasil.infrastructure.hitomila import HitomiLa

from tests.conftest import *


@pytest_asyncio.fixture
async def hitomi_la():
    hitomi_la = await HitomiLa.create(["index-english.nozomi"])
    yield hitomi_la
    await hitomi_la.session.close()


@pytest.mark.asyncio
async def test_image_not_in_local(asgi_client: httpx.AsyncClient, hitomi_la: HitomiLa):
    response = await asgi_client.get("/api/hitomi/image/1")
    assert response.status_code == 200
    resolved = ResolvedImage.from_dict(response.json()[0])
    async with httpx.AsyncClient() as client:
        image_response = await client.get(resolved.url, headers=hitomi_la.headers)
    assert image_response.status_code == 200


@pytest.mark.asyncio
async def test_image_in_local(
    asgi_client: httpx.AsyncClient, sample_galleryinfo: Galleryinfo, hitomi_la: HitomiLa
):
    response = await asgi_client.get(f"/api/hitomi/image/{sample_galleryinfo.id}")
    assert response.status_code == 200
    resolved = ResolvedImage.from_dict(response.json()[0])
    async with httpx.AsyncClient() as client:
        image_response = await client.get(resolved.url, headers=hitomi_la.headers)
    assert image_response.status_code == 200


@pytest.mark.asyncio
async def test_image_not_found(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/image/999999999")
    assert response.status_code == 404
