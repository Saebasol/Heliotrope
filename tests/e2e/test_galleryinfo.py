import httpx
import pytest
from yggdrasil.domain.entities.galleryinfo import Galleryinfo

from tests.conftest import *


@pytest.mark.asyncio
async def test_galleryinfo_not_in_local(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/galleryinfo/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_galleryinfo_in_local(
    asgi_client: httpx.AsyncClient, sample_galleryinfo: Galleryinfo
):
    response = await asgi_client.get(f"/api/hitomi/galleryinfo/{sample_galleryinfo.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_galleryinfo.id


@pytest.mark.asyncio
async def test_galleryinfo_not_found(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/galleryinfo/999999999")
    assert response.status_code == 404
