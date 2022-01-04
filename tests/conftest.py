import json
from asyncio.events import AbstractEventLoop, get_running_loop, new_event_loop
from tests.common import galleryinfo
from pytest import fixture, mark
from sanic_ext.extensions.http.extension import HTTPExtension
from sanic_ext.extensions.injection.extension import InjectionExtension
from sanic_ext.extensions.openapi.extension import OpenAPIExtension
from sanic_testing import TestManager  # type:ignore

from heliotrope.config import HeliotropeConfig
from heliotrope.database.orm.base import mapper_registry
from heliotrope.domain.galleryinfo import Galleryinfo
from heliotrope.domain.info import Info
from heliotrope.interpreter import CommonJS
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.sanic import Heliotrope
from heliotrope.server import create_app
from tests.common import galleryinfo, info


class LoopThatIsNeverClosed(AbstractEventLoop):
    def __init__(self):
        self._loop = None

    def __getattribute__(self, name: str):
        if name == "_loop":
            return super().__getattribute__("_loop")
        if self._loop is None or self._loop.is_closed():
            self._loop = new_event_loop()
        return getattr(self._loop, name)


def get_config():
    with open("./tests/config.json", "r") as f:
        config = HeliotropeConfig()
        config.update(json.load(f))
        return config


async def startup_test(heliotrope: Heliotrope, loop: AbstractEventLoop):
    await heliotrope.ctx.orm.add_galleryinfo(Galleryinfo.from_dict(galleryinfo))
    await heliotrope.ctx.meilisearch.add_infos([Info.from_dict(info)])


async def closeup_test(heliotrope: Heliotrope, loop: AbstractEventLoop):
    async with heliotrope.ctx.orm.engine.begin() as connection:
        await connection.run_sync(mapper_registry.metadata.drop_all)
    await heliotrope.ctx.meilisearch.index.delete()


@fixture
def event_loop():
    loop = LoopThatIsNeverClosed()
    yield loop
    loop.close()


@fixture
def app():
    heliotrope_config = get_config()
    heliotrope = create_app(heliotrope_config)
    TestManager(heliotrope)
    heliotrope.main_process_start(startup_test)
    heliotrope.main_process_stop(closeup_test)
    yield heliotrope


@fixture(autouse=True)
def reset_extensions():
    yield
    for ext in (HTTPExtension, InjectionExtension, OpenAPIExtension):
        ext._singleton = None


@fixture
@mark.asyncio
async def image_url():
    hitomi_request = await HitomiRequest.setup()
    common_js = await CommonJS.setup(hitomi_request)
    yield await common_js.use_document_title(
        galleryinfo["id"],
        galleryinfo["files"][0],
        True,
        "Sekigahara-san wa Dasaretai | 세키가하라는 발산하고싶어 | Hitomi.la",
    )


@fixture
@mark.asyncio
async def fake_app():
    heliotrope_config = get_config()
    heliotrope = create_app(heliotrope_config)
    heliotrope.main_process_stop(closeup_test)
    # do not run app
    for listener in heliotrope.listeners["main_process_start"]:
        # None is loop argument but not needed
        await listener(heliotrope, None)
    # return app
    yield heliotrope
    for listener in heliotrope.listeners["main_process_stop"]:
        await listener(heliotrope, None)
