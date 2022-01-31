from asyncio import TimeoutError, wait_for
from asyncio.events import AbstractEventLoop

from pytest import mark

from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import MirroringTask


@mark.timeout(120)
@mark.flaky(reruns=5, reruns_delay=5)
def test_mirroring_task(fake_app: Heliotrope, event_loop: AbstractEventLoop):
    try:
        event_loop.run_until_complete(wait_for(MirroringTask.setup(fake_app, 5), 15))
    except TimeoutError:
        info_total = event_loop.run_until_complete(fake_app.ctx.odm.get_all_index())
        galleryinfo_total = event_loop.run_until_complete(
            fake_app.ctx.orm.get_all_index()
        )
        assert len(galleryinfo_total) >= 1
        assert len(info_total) >= 1
