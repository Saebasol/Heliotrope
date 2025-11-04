import httpx
import pytest
from yggdrasil.application.dtos.search import SearchResultDTO


@pytest.mark.asyncio
async def test_search(asgi_client: httpx.AsyncClient):
    response = await asgi_client.post(
        "/api/hitomi/search?offset=1", json={"query": ["artist:tamano_kedama"]}
    )
    assert response.status_code == 200
    result = SearchResultDTO(**response.json())
    assert isinstance(result.results, list)
    assert isinstance(result.count, int)


@pytest.mark.asyncio
async def test_search_negative(asgi_client: httpx.AsyncClient):
    response = await asgi_client.post(
        "/api/hitomi/search?offset=-1", json={"query": ["artist:tamano_kedama"]}
    )
    assert response.status_code == 200
    result = SearchResultDTO(**response.json())
    assert isinstance(result.results, list)
    assert isinstance(result.count, int)
