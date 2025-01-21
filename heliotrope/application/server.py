from asyncio import AbstractEventLoop
from heliotrope.application.config import HeliotropeConfig
from heliotrope.application.javascript.interpreter import JavaScriptInterpreter
from heliotrope.application.sanic import Heliotrope
from heliotrope.application.tasks.mirroring import MirroringTask
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.mongodb.info import MongoDB
from heliotrope.infrastructure.mongodb.info.domain.repository import (
    MongoDBInfoRepository,
)
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy

from heliotrope.infrastructure.hitomila.galleryinfo.domain.repository import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.repository import (
    SAGalleryinfoRepository,
)

from heliotrope.application.endpoint import endpoint


async def startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
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

    heliotrope.ctx.mirroring_task = MirroringTask(
        heliotrope.ctx.hitomi_la_galleryinfo_repository,
        heliotrope.ctx.sa_galleryinfo_repository,
        heliotrope.ctx.mongodb_repository,
    )

    heliotrope.add_task(
        heliotrope.ctx.mirroring_task.start(heliotrope.config.MIRRORING_DELAY)
    )


async def closeup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Close session
    await heliotrope.ctx.mongodb.client.close()
    await heliotrope.ctx.sa.engine.dispose()
    await heliotrope.ctx.hitomi_la.session.close()

    # Close task
    heliotrope.shutdown_tasks()


def create_app(config: HeliotropeConfig) -> Heliotrope:
    heliotrope = Heliotrope("heliotrope")
    heliotrope.config.update(config)
    heliotrope.blueprint(endpoint)
    heliotrope.before_server_start(startup)
    heliotrope.before_server_stop(closeup)

    return heliotrope
