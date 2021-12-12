from asyncio.events import AbstractEventLoop
from asyncio.tasks import all_tasks, current_task

from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration

from heliotrope.config import HeliotropeConfig
from heliotrope.database.meilisearch.client import MeiliSearch
from heliotrope.database.orm import ORM
from heliotrope.interpreter import CommonJS
from heliotrope.request.base import BaseRequest
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.rest import rest
from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import MirroringTask
from heliotrope.tasks.refresh import RefreshCommonJS


async def startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Sentry
    if not heliotrope.config.TESTING:
        init(heliotrope.config.SENTRY_DSN, integrations=[SanicIntegration()])
        # Task setup
        heliotrope.add_task(
            MirroringTask.setup(heliotrope, heliotrope.config.MIRRORING_DELAY)
        )
        heliotrope.add_task(
            RefreshCommonJS.setup(heliotrope, heliotrope.config.REFRESH_COMMON_JS_DELAY)
        )

    # DB and http setup
    heliotrope.ctx.meilisearch = await MeiliSearch.setup(heliotrope.config.INFO_DB_URL)
    heliotrope.ctx.orm = await ORM.setup(heliotrope.config.GALLERYINFO_DB_URL)
    heliotrope.ctx.request = await BaseRequest.setup()
    heliotrope.ctx.hitomi_request = await HitomiRequest.setup(
        index_file=heliotrope.config.INDEX_FILE
    )
    heliotrope.ctx.common_js = await CommonJS.setup(heliotrope.ctx.hitomi_request)


async def closeup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Close session
    await heliotrope.ctx.meilisearch.close()
    await heliotrope.ctx.request.close()
    await heliotrope.ctx.hitomi_request.request.close()

    # Close task
    current = current_task()
    for task in all_tasks():
        if task is not current:
            task.cancel()


def create_app(config: HeliotropeConfig) -> Heliotrope:
    heliotrope = Heliotrope("heliotrope")
    heliotrope.config.update(config)

    heliotrope.blueprint(rest)

    heliotrope.main_process_start(startup)
    heliotrope.main_process_stop(closeup)

    return heliotrope
