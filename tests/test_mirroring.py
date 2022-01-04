from asyncio import wait_for, TimeoutError, create_task

from pytest import mark

from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import MirroringTask


@mark.asyncio
@mark.timeout(120)
@mark.flaky(reruns=3, reruns_delay=5)
async def test_mirroring_task(fake_app: Heliotrope):
    try:
        await wait_for(create_task(MirroringTask.setup(fake_app, 5)), 10)
    except TimeoutError:
        stats = await fake_app.ctx.meilisearch.index.get_stats()
        info_total = stats["numberOfDocuments"]
        galleryinfo_total = await fake_app.ctx.orm.get_all_index()
        assert len(galleryinfo_total) >= 1
        assert info_total >= 1
