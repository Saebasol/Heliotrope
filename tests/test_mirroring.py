from asyncio import sleep

from pytest import mark

from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import MirroringTask


@mark.asyncio
async def test_mirroring_task(fake_app: Heliotrope):
    await MirroringTask.setup(fake_app, 5)
    await sleep(10)
    stats = await fake_app.ctx.meilisearch.index.get_stats()
    info_total = stats["numberOfDocuments"]
    galleryinfo_total = await fake_app.ctx.orm.get_all_index()
    assert len(galleryinfo_total) >= 1
    assert info_total >= 1
