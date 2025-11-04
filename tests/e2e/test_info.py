import httpx
import pytest
from yggdrasil.domain.entities.info import Info

from tests.unit.domain.entities.conftest import *


@pytest.mark.asyncio
async def test_info_not_in_local(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/info/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_info_in_local(asgi_client: httpx.AsyncClient, sample_info: Info):
    response = await asgi_client.get(f"/api/hitomi/info/{sample_info.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_info.id


@pytest.mark.asyncio
async def test_info_not_found(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/info/999999999")
    assert response.status_code == 404
