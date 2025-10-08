import httpx
import pytest


@pytest.mark.asyncio
async def test_root(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/")
    assert response.status_code == 302
