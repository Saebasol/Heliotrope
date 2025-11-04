import pytest_asyncio
from yggdrasil.infrastructure.hitomila import HitomiLa


@pytest_asyncio.fixture
async def hitomi_la():
    hitomi_la = await HitomiLa.create(["index-english.nozomi"])
    yield hitomi_la
    await hitomi_la.session.close()
