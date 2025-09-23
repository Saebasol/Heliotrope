import httpx
import pytest


@pytest.mark.asyncio
async def test_galleryinfo(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/galleryinfo/1")
    assert response.status_code == 200
    print(response.json())
