import pytest_asyncio
from yggdrasil.infrastructure.hitomila import HitomiLa
from yggdrasil.infrastructure.pythonmonkey import JavaScriptInterpreter

from tests.integration.infrastructure.hitomila.conftest import hitomi_la as hitomi_la


@pytest_asyncio.fixture()
async def javascript_interpreter(hitomi_la: HitomiLa):
    interpreter = await JavaScriptInterpreter.setup(hitomi_la)
    yield interpreter
