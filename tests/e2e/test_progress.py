import httpx
import pytest


@pytest.mark.asyncio
async def test_status(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/status")
    assert response.status_code == 200
    body = response.json()
    assert "index_files" in body
