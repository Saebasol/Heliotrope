import httpx
import pytest


@pytest.mark.asyncio
async def test_random(asgi_client: httpx.AsyncClient):
    response = await asgi_client.post(
        "/api/hitomi/random", json={"query": ["artist:tamano_kedama"]}
    )
    assert response.status_code == 200
    assert response.json()["artists"][0] == "tamano_kedama"
