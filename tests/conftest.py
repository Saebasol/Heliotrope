import json
import os

from _pytest.config import Config
from pytest import fixture
from sanic.app import Sanic
from sanic_testing import TestManager  # type:ignore
from tortoise import Tortoise, run_async

from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.hitomi.models import HitomiGalleryinfo
from heliotrope.server import heliotrope
from tests.case import galleryinfo, info


def get_config():
    with open("./tests/config.json", "r") as f:
        return json.load(f)


def pytest_configure(config: Config):
    async def query():
        mongo = NoSQLQuery(get_config()["nosql"])
        await Tortoise.init(
            db_url=os.environ["DB_URL"],
            modules={
                "models": [
                    "heliotrope.database.models.hitomi",
                ]
            },
        )
        await Tortoise.generate_schemas()
        orm = SQLQuery()
        await orm.add_galleryinfo(HitomiGalleryinfo(galleryinfo))
        await mongo.insert_info(info)

    run_async(query())


@fixture()
def app() -> Sanic:
    heliotrope.update_config(get_config())
    TestManager(heliotrope)
    return heliotrope
