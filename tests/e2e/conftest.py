import httpx
import pytest_asyncio
from sanic import Sanic

from heliotrope.infrastructure.sanic.app import Heliotrope
from heliotrope.infrastructure.sanic.bootstrap import create_app, main_process_startup
from heliotrope.infrastructure.sanic.config import HeliotropeConfig

ASGI_HOST = "mockserver"
ASGI_PORT = 1234
ASGI_BASE_URL = f"http://{ASGI_HOST}:{ASGI_PORT}"
HOST = "127.0.0.1"
PORT = None


@pytest_asyncio.fixture()
async def heliotrope():
    Sanic.test_mode = True
    config = HeliotropeConfig()
    config.load_config_with_config_json("tests/config.json")
    heliotrope = create_app(config)
    heliotrope.asgi = True
    yield heliotrope
    Sanic.test_mode = False


@pytest_asyncio.fixture()
async def asgi_client(heliotrope: Heliotrope):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=heliotrope, client=(ASGI_HOST, ASGI_PORT)),
        base_url=ASGI_BASE_URL,
        headers={"Host": f"{ASGI_HOST}:{ASGI_PORT}"},
    ) as client:
        heliotrope.router.reset()
        heliotrope.signal_router.reset()
        await heliotrope._startup()
        await main_process_startup(heliotrope, None)  # type: ignore
        await heliotrope._server_event("init", "before")
        await heliotrope._server_event("init", "after")
        yield client
        await heliotrope._server_event("shutdown", "before")
        await heliotrope._server_event("shutdown", "after")
