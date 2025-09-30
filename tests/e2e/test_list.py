import httpx
import pytest

from heliotrope.application.dtos.list import ListResultDTO


@pytest.mark.asyncio
async def test_list(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/list/1")
    assert response.status_code == 200
    result = ListResultDTO(**response.json())
    assert isinstance(result.count, int)
    assert isinstance(result.items, list)


@pytest.mark.asyncio
async def test_list_negative(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/list/-1")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_over(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/list/9999999")
    assert response.status_code == 400
