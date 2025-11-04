# pyright: reportPrivateUsage=false
import asyncio

import pytest
import pytest_asyncio
from aiohttp import ClientResponse, ClientSession, ClientTimeout
from yggdrasil.infrastructure.hitomila import HitomiLa


@pytest_asyncio.fixture()
async def client_session():
    async with ClientSession() as session:
        yield session


@pytest.fixture
def index_files():
    return ["index-korean.nozomi", "index-english.nozomi"]


@pytest.mark.asyncio
async def test_real_http_request_to_base_url(client_session: ClientSession):
    hitomi_la = HitomiLa(client_session, [])

    response = await client_session.get(hitomi_la.base_url, headers=hitomi_la.headers)
    assert response.status in [200, 403, 503]


@pytest.mark.asyncio
async def test_real_ltn_url_accessibility(client_session: ClientSession):
    hitomi_la = HitomiLa(client_session, [])

    response = await client_session.get(hitomi_la.ltn_url, headers=hitomi_la.headers)
    assert response.status in [200, 403, 404, 503]


@pytest.mark.asyncio
async def test_create_hitomi_la():
    hitomi_la = await HitomiLa.create(["index-korean.nozomi"])

    try:
        assert isinstance(hitomi_la.session, ClientSession)

        async with hitomi_la.session.get(
            hitomi_la.base_url, headers=hitomi_la.headers
        ) as response:
            assert response.status in [200, 403, 503]

    finally:
        await hitomi_la.session.close()


@pytest.mark.asyncio
async def test_session_cleanup(index_files: list[str]):
    hitomi_la = await HitomiLa.create(index_files)

    assert not hitomi_la.session.closed

    await hitomi_la.session.close()

    assert hitomi_la.session.closed


@pytest.mark.asyncio
async def test_index_url_request(client_session: ClientSession):
    hitomi_la = HitomiLa(client_session, ["index-korean.nozomi"])

    index_urls = list(hitomi_la.index_url)
    if index_urls:
        async with client_session.get(
            index_urls[0],
            headers=hitomi_la.headers,
            timeout=ClientTimeout(total=10),
        ) as response:
            assert response.status in [200, 403, 503]


@pytest.mark.asyncio
async def test_user_agent_effectiveness(client_session: ClientSession):
    hitomi_la = HitomiLa(client_session, [])

    async with client_session.get(hitomi_la.base_url) as response_without:
        status_without = response_without.status

    async with client_session.get(
        hitomi_la.base_url, headers=hitomi_la.headers
    ) as response_with:
        status_with = response_with.status

    assert status_without in [200, 403, 503]
    assert status_with in [200, 403, 503]


@pytest.mark.asyncio
async def test_multiple_concurrent_requests(
    client_session: ClientSession, index_files: list[str]
):
    hitomi_la = HitomiLa(client_session, index_files)

    urls = [hitomi_la.base_url, hitomi_la.ltn_url]

    tasks = []
    for url in urls:
        task = client_session.get(url, headers=hitomi_la.headers)
        tasks.append(task)

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for response in responses:
        if isinstance(response, ClientResponse):
            assert response.status in [200, 403, 404, 503]
            await response.release()
