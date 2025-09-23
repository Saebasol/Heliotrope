import httpx
import pytest_asyncio
from sanic import Sanic

from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.info import Info
from heliotrope.infrastructure.sanic.app import Heliotrope
from heliotrope.infrastructure.sanic.bootstrap import create_app, main_process_startup
from heliotrope.infrastructure.sanic.config import HeliotropeConfig
from tests.unit.domain.entities.conftest import *

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
async def asgi_client(
    heliotrope: Heliotrope, sample_galleryinfo: Galleryinfo, sample_info: Info
):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=heliotrope, client=(ASGI_HOST, ASGI_PORT)),
        base_url=ASGI_BASE_URL,
        headers={"Host": f"{ASGI_HOST}:{ASGI_PORT}"},
    ) as client:
        heliotrope.router.reset()
        heliotrope.signal_router.reset()
        await heliotrope._startup()
        await main_process_startup(heliotrope, None)
        await heliotrope._server_event("init", "before")
        await heliotrope._server_event("init", "after")
        # Add sample data to the repositories
        await heliotrope.ctx.sa_galleryinfo_repository.add_galleryinfo(
            sample_galleryinfo
        )
        await heliotrope.ctx.mongodb_repository.add_info(sample_info)
        yield client
        # Clean up the sample data from the repositories
        await heliotrope.ctx.sa_galleryinfo_repository.delete_galleryinfo(
            sample_galleryinfo.id
        )
        await heliotrope.ctx.mongodb_repository.delete_info(sample_info.id)
        await heliotrope._server_event("shutdown", "before")
        await heliotrope._server_event("shutdown", "after")
