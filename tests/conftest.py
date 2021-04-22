import json
import os

import aiohttp
import pytest
from sanic_testing import TestManager
from tortoise import Tortoise, run_async

from heliotrope.database.models.hitomi import File, GalleryInfo, Index, Tag
from heliotrope.server import heliotrope_app
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel


def pytest_configure(config):
    async def query_db():
        await Tortoise.init(
            db_url=os.environ["DB_URL"],
            modules={
                "models": [
                    "heliotrope.database.models.hitomi",
                    "heliotrope.database.models.requestcount",
                ]
            },
        )
        await Tortoise.generate_schemas()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://ltn.hitomi.la/galleries/1536576.js",
                headers={"referer": "http://hitomi.la"},
            ) as r:
                js_to_json = (await r.text()).replace("var galleryinfo = ", "")
                galleryinfo = HitomiGalleryInfoModel.parse_galleryinfo(
                    json.loads(js_to_json)
                )

        galleyinfo_orm_object = await GalleryInfo.create(
            language_localname=galleryinfo.language_localname,
            language=galleryinfo.language,
            date=galleryinfo.date,
            japanese_title=galleryinfo.japanese_title,
            title=galleryinfo.title,
            id=galleryinfo.galleryid,
            type=galleryinfo.hitomi_type,
        )

        if galleryinfo.files:
            file_orm_object_list = []
            for file_info in galleryinfo.files:
                file_orm_object = File(
                    index_id=galleryinfo.galleryid,
                    width=file_info.get("width"),
                    hash=file_info.get("hash"),
                    haswebp=file_info.get("haswebp"),
                    name=file_info.get("name"),
                    height=file_info.get("height"),
                )
                await file_orm_object.save()
                file_orm_object_list.append(file_orm_object)
            await galleyinfo_orm_object.files.add(*file_orm_object_list)

        if galleryinfo.tags:
            tag_orm_object_list = []
            for tag_info in galleryinfo.tags:
                tag_orm_object = Tag(
                    index_id=galleryinfo.galleryid,
                    male=tag_info.get("male"),
                    female=tag_info.get("female"),
                    url=tag_info.get("url"),
                )
                await tag_orm_object.save()
                tag_orm_object_list.append(tag_orm_object)

            await galleyinfo_orm_object.tags.add(*tag_orm_object_list)

        await Index.create(index_id="1536576")

    run_async(query_db())


@pytest.fixture
def app():
    TestManager(heliotrope_app)
    return heliotrope_app
