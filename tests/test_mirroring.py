from heliotrope.tasks.mirroring import MirroringTask
from heliotrope.sanic import Heliotrope
from asyncio import sleep
from pytest import mark


@mark.asyncio
async def test_mirroring_task(fake_app: Heliotrope):
    await MirroringTask.setup(fake_app, 5)
    await sleep(5)
    stats = await fake_app.ctx.meilisearch.index.get_stats()
    info_total = stats["numberOfDocuments"]
    galleryinfo_total = await fake_app.ctx.orm.get_all_index()
    assert len(galleryinfo_total) >= 2
    assert info_total >= 2
