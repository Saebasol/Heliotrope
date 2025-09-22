from importlib import reload

import pytest_asyncio
from pythonmonkey import eval, stop  # pyright: ignore[reportMissingTypeStubs]

from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.pythonmonkey import JavaScriptInterpreter
from tests.integration.hitomila.conftest import hitomi_la as hitomi_la


@pytest_asyncio.fixture()
async def javascript_interpreter(hitomi_la: HitomiLa):
    interpreter = await JavaScriptInterpreter.setup(hitomi_la)
    yield interpreter
