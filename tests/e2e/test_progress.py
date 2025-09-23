import httpx
import pytest


@pytest.mark.asyncio
async def test_progress(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/progress")
    assert response.status_code == 200
    body = response.json()
    assert "index_files" in body
