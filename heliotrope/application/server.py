from asyncio import AbstractEventLoop
from heliotrope.application.config import HeliotropeConfig
from heliotrope.application.sanic import Heliotrope
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy

from heliotrope.infrastructure.hitomila.galleryinfo.domain.repository import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.repository import (
    SAGalleryinfoRepository,
)

from heliotrope.application.api import api_endpoint


async def startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    heliotrope.ctx.sa = await SQLAlchemy.create(heliotrope.config.GALLERYINFO_DB_URL)
    heliotrope.ctx.hitomi_la = await HitomiLa.create(heliotrope.config.INDEX_FILES)

    heliotrope.ctx.hitomi_la_galleryinfo_repository = HitomiLaGalleryinfoRepository(
        heliotrope.ctx.hitomi_la
    )
    heliotrope.ctx.sa_galleryinfo_repository = SAGalleryinfoRepository(
        heliotrope.ctx.sa
    )


async def closeup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Close session
    await heliotrope.ctx.sa.engine.dispose()
    await heliotrope.ctx.hitomi_la.session.close()

    # Close task
    heliotrope.shutdown_tasks()


def create_app(config: HeliotropeConfig) -> Heliotrope:
    heliotrope = Heliotrope("heliotrope")
    heliotrope.config.update(config)
    heliotrope.blueprint(api_endpoint)
    heliotrope.before_server_start(startup)
    heliotrope.before_server_stop(closeup)

    return heliotrope
