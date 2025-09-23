import httpx
import pytest


@pytest.mark.asyncio
async def test_proxy(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/image/1")
    assert response.status_code == 200
    proxy_response = await asgi_client.get(f"/api/proxy/{response.json()[0]['url']}")
    assert proxy_response.status_code == 200
