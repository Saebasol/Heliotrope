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


def pytest_configure(config: Config):
    async def query():
        mongo = NoSQLQuery(os.environ["MONGO_DB_URL"])
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
    TestManager(heliotrope)
    return heliotrope
