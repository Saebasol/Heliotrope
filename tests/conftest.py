import json
from asyncio.events import AbstractEventLoop, get_running_loop, new_event_loop

from pytest import fixture, mark
from sanic_ext.extensions.http.extension import HTTPExtension
from sanic_ext.extensions.injection.extension import InjectionExtension
from sanic_ext.extensions.openapi.extension import OpenAPIExtension
from sanic_testing import TestManager  # type:ignore

from heliotrope.config import HeliotropeConfig
from heliotrope.database.orm.base import mapper_registry
from heliotrope.domain.galleryinfo import Galleryinfo
from heliotrope.domain import Info, Galleryinfo
from heliotrope.js.common import Common
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.sanic import Heliotrope
from heliotrope.server import create_app
from tests.common import galleryinfo, info


def get_config():
    with open("./tests/config.json", "r") as f:
        config = HeliotropeConfig()
        config.update(json.load(f))
        return config


async def startup_test(heliotrope: Heliotrope, loop: AbstractEventLoop):
    await heliotrope.ctx.orm.add_galleryinfo(Galleryinfo.from_dict(galleryinfo))
    await heliotrope.ctx.odm.add_info(Info.from_dict(info))


async def closeup_test(heliotrope: Heliotrope, loop: AbstractEventLoop):
    async with heliotrope.ctx.orm.engine.begin() as connection:
        await connection.run_sync(mapper_registry.metadata.drop_all)
    await heliotrope.ctx.odm.collection.delete_many({})


@fixture
def app():
    heliotrope_config = get_config()
    heliotrope = create_app(heliotrope_config)
    TestManager(heliotrope)
    heliotrope.before_server_start(startup_test)
    heliotrope.before_server_stop(closeup_test)
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
    code = await hitomi_request.get_gg_js()
    common_js = Common.setup(code)
    gi = Galleryinfo.from_dict(galleryinfo)
    yield common_js.url_from_url_from_hash(str(gi.id), gi.files[0], "webp", "", "a")


@fixture
@mark.asyncio
async def fake_app():
    heliotrope_config = get_config()
    heliotrope = create_app(heliotrope_config)

    before_server_start = []
    before_server_stop = []
    # Apply listeners
    before_server_stop.append(closeup_test)
    for future_listener in heliotrope._future_listeners:
        if future_listener.event == "before_server_start":
            before_server_start.append(future_listener.listener)
        else:
            before_server_stop.append(future_listener.listener)

    # do not run app
    for listener in before_server_start:
        # None is loop argument but not needed
        await listener(heliotrope, None)
    # return app
    yield heliotrope
    for listener in before_server_stop:
        await listener(heliotrope, None)
