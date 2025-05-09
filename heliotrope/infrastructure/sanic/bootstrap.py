from asyncio import AbstractEventLoop
from multiprocessing import Lock, Manager

from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration

from heliotrope import __version__
from heliotrope.adapters.endpoint import endpoint
from heliotrope.application.javascript.interpreter import JavaScriptInterpreter
from heliotrope.application.tasks.mirroring import MirroringProgress, MirroringTask
from heliotrope.application.tasks.refresh import RefreshggJS
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.hitomila.repositories.galleryinfo import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.mongodb import MongoDB
from heliotrope.infrastructure.mongodb.repositories.info import MongoDBInfoRepository
from heliotrope.infrastructure.sanic.app import Heliotrope
from heliotrope.infrastructure.sanic.config import HeliotropeConfig
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)


async def main_process_startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    manager = Manager()
    heliotrope.shared_ctx.namespace = manager.Namespace()
    heliotrope.shared_ctx.mirroring_progress_dict = manager.dict()
    heliotrope.shared_ctx.mirroring_progress_dict.update(
        MirroringProgress.default().to_dict()
    )
    heliotrope.shared_ctx.namespace.is_running = False


async def startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    if heliotrope.config.PRODUCTION:
        init(
            heliotrope.config.SENTRY_DSN,
            integrations=[SanicIntegration()],
            release=__version__,
        )

    heliotrope.ctx.sa = await SQLAlchemy.create(heliotrope.config.GALLERYINFO_DB_URL)
    heliotrope.ctx.hitomi_la = await HitomiLa.create(heliotrope.config.INDEX_FILES)
    heliotrope.ctx.mongodb = await MongoDB.create(heliotrope.config.INFO_DB_URL)

    heliotrope.ctx.hitomi_la_galleryinfo_repository = HitomiLaGalleryinfoRepository(
        heliotrope.ctx.hitomi_la
    )
    heliotrope.ctx.sa_galleryinfo_repository = SAGalleryinfoRepository(
        heliotrope.ctx.sa
    )
    heliotrope.ctx.mongodb_repository = MongoDBInfoRepository(
        heliotrope.ctx.mongodb, heliotrope.config.USE_ATLAS_SEARCH
    )

    heliotrope.ctx.javascript_interpreter = await JavaScriptInterpreter.setup(
        heliotrope.ctx.hitomi_la
    )

    refresh_gg_js = RefreshggJS(heliotrope)

    heliotrope.add_task(
        refresh_gg_js.start(heliotrope.config.REFRESH_GG_JS_DELAY),
    )

    with Lock():
        namespace = heliotrope.shared_ctx.namespace
        mirroring_progress_dict = heliotrope.shared_ctx.mirroring_progress_dict

        if not namespace.is_running:
            mirroring_task = MirroringTask(
                heliotrope.ctx.hitomi_la_galleryinfo_repository,
                heliotrope.ctx.sa_galleryinfo_repository,
                heliotrope.ctx.mongodb_repository,
                mirroring_progress_dict,
            )

            heliotrope.add_task(mirroring_task.start(heliotrope.config.MIRRORING_DELAY))
            namespace.is_running = True


async def closeup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Close session
    await heliotrope.ctx.mongodb.client.close()
    await heliotrope.ctx.sa.engine.dispose()
    await heliotrope.ctx.hitomi_la.session.close()
    heliotrope.shutdown_tasks()


def create_app(config: HeliotropeConfig) -> Heliotrope:
    heliotrope = Heliotrope("heliotrope")
    heliotrope.config.update(config)
    heliotrope.blueprint(endpoint)
    heliotrope.main_process_start(main_process_startup)
    heliotrope.before_server_start(startup)
    heliotrope.before_server_stop(closeup)

    return heliotrope
