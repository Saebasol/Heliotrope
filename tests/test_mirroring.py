from asyncio import TimeoutError, wait_for
from asyncio.events import AbstractEventLoop

from pytest import mark

from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import MirroringTask


@mark.asyncio
@mark.timeout(120)
@mark.flaky(reruns=5, reruns_delay=5)
async def test_mirroring_task(fake_app: Heliotrope, event_loop: AbstractEventLoop):
    try:
        await wait_for(MirroringTask.setup(fake_app, 5), 5)
    except TimeoutError:
        info_total = await fake_app.ctx.odm.get_all_index()
        galleryinfo_total = await fake_app.ctx.orm.get_all_index()

        assert len(galleryinfo_total) >= 1
        assert len(info_total) >= 1
