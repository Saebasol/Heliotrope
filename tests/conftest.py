from asyncio.events import AbstractEventLoop
import json

from pytest import fixture
from pytest import mark
from sanic_testing import TestManager  # type:ignore
from heliotrope.sanic import Heliotrope
from heliotrope.config import HeliotropeConfig
from heliotrope.domain.galleryinfo import Galleryinfo
from heliotrope.domain.info import Info
from tests.common import galleryinfo, info
from heliotrope.server import create_app
from heliotrope.database.orm.base import mapper_registry


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
@mark.asyncio
async def app():
    heliotrope_config = get_config()
    heliotrope = create_app(heliotrope_config)
    TestManager(heliotrope)
    heliotrope.main_process_start(startup_test)
    heliotrope.main_process_stop(closeup_test)
    yield heliotrope


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
