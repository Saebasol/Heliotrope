import httpx
import pytest


@pytest.mark.asyncio
async def test_thumbnail_multiple(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get(
        "/api/hitomi/thumbnail/1?size=smallsmall&single=false"
    )
    assert response.status_code == 200
    assert len(response.json()) >= 2
    thumbnail_response = await asgi_client.get(
        f"/api/proxy/{response.json()[0]['url']}"
    )

    assert thumbnail_response.status_code == 200


@pytest.mark.asyncio
async def test_thumbnail_smallsmall(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get(
        "/api/hitomi/thumbnail/1?size=smallsmall&single=true"
    )
    assert response.status_code == 200
    thumbnail_response = await asgi_client.get(
        f"/api/proxy/{response.json()[0]['url']}"
    )
    assert thumbnail_response.status_code == 200


@pytest.mark.asyncio
async def test_thumbnail_small(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/thumbnail/1?size=small&single=true")
    assert response.status_code == 200
    thumbnail_response = await asgi_client.get(
        f"/api/proxy/{response.json()[0]['url']}"
    )
    assert thumbnail_response.status_code == 200


@pytest.mark.asyncio
async def test_thumbnail_smallbig(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get(
        "/api/hitomi/thumbnail/1?size=smallbig&single=true"
    )
    assert response.status_code == 200
    thumbnail_response = await asgi_client.get(
        f"/api/proxy/{response.json()[0]['url']}"
    )
    assert thumbnail_response.status_code == 200


@pytest.mark.asyncio
async def test_thumbnail_big(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/thumbnail/1?size=big&single=true")
    assert response.status_code == 200
    thumbnail_response = await asgi_client.get(
        f"/api/proxy/{response.json()[0]['url']}"
    )
    assert thumbnail_response.status_code == 200
