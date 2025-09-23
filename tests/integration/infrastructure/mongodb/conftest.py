import json

import pytest
import pytest_asyncio

from heliotrope.infrastructure.mongodb import MongoDB


@pytest.fixture()
def db_url() -> str:
    with open("tests/config.json") as f:
        config = json.load(f)
    return config["INFO_DB_URL"]


@pytest_asyncio.fixture()
async def mongodb(db_url: str):
    mongodb = await MongoDB.create(db_url)
    yield mongodb
    await mongodb.collection.drop()
    await mongodb.client.close()
