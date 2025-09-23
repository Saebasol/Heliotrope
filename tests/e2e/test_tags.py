import httpx
import pytest


@pytest.mark.asyncio
async def test_tags(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/tags")
    assert response.status_code == 200
    assert response.json()["artists"][0] == "tamano_kedama"
