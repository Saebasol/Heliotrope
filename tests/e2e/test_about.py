import httpx
import pytest


@pytest.mark.asyncio
async def test_about(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/about")
    assert response.status_code == 200
