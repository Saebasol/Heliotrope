from asyncio import AbstractEventLoop
from multiprocessing import Lock, Manager

from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration

from heliotrope import __version__
from heliotrope.adapters.endpoint import endpoint
from heliotrope.application.javascript.interpreter import JavaScriptInterpreter
from heliotrope.application.javascript.thumbnail import ThumbnailResolver
from heliotrope.application.tasks.manager import TaskManager
from heliotrope.application.tasks.mirroring import MirroringProgress, MirroringTask
from heliotrope.application.tasks.refresh import RefreshggJS
from heliotrope.domain.exceptions import GalleryinfoNotFound, InfoNotFound
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.hitomila.repositories.galleryinfo import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.mongodb import MongoDB
from heliotrope.infrastructure.mongodb.repositories.info import MongoDBInfoRepository
from heliotrope.infrastructure.sanic.app import Heliotrope
from heliotrope.infrastructure.sanic.config import HeliotropeConfig
from heliotrope.infrastructure.sanic.error import not_found
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
    heliotrope.shared_ctx.namespace.is_running_first_process = False


async def startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    if heliotrope.config.PRODUCTION:
        init(
            heliotrope.config.SENTRY_DSN,
            integrations=[SanicIntegration()],
            release=__version__,
            ignore_errors=[
                GalleryinfoNotFound,
                InfoNotFound,
            ],
            traces_sample_rate=1.0,
            profile_session_sample_rate=1.0,
            profile_lifecycle="trace",
        )

    heliotrope.ctx.sa = SQLAlchemy.create(heliotrope.config.GALLERYINFO_DB_URL)
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
    heliotrope.ctx.thumbnail_resolver = ThumbnailResolver(
        heliotrope.ctx.javascript_interpreter
    )

    refresh_gg_js = RefreshggJS(heliotrope)
    task_manager = TaskManager(heliotrope)

    task_manager.register_task(
        refresh_gg_js.start,
        RefreshggJS.__name__,
        heliotrope.config.REFRESH_GG_JS_DELAY,
    )

    with Lock():
        namespace = heliotrope.shared_ctx.namespace
        mirroring_progress_dict = heliotrope.shared_ctx.mirroring_progress_dict

        if not namespace.is_running_first_process:
            namespace.is_running_first_process = True
            await heliotrope.ctx.sa.create_all_table()
            await heliotrope.ctx.mongodb.collection.create_index([("id", -1)])
            if heliotrope.ctx.mongodb.is_atlas and heliotrope.config.USE_ATLAS_SEARCH:
                await heliotrope.ctx.mongodb.collection.create_search_index(
                    {
                        "name": "default",
                        "definition": {
                            "mappings": {
                                "dynamic": True,
                                "fields": {
                                    "title": {
                                        "analyzer": "lucene.korean",
                                        "searchAnalyzer": "lucene.korean",
                                        "type": "string",
                                    }
                                },
                            }
                        },
                    }
                )
            mirroring_task = MirroringTask(
                heliotrope.ctx.hitomi_la_galleryinfo_repository,
                heliotrope.ctx.sa_galleryinfo_repository,
                heliotrope.ctx.mongodb_repository,
                mirroring_progress_dict,
            )
            mirroring_task.REMOTE_CONCURRENT_SIZE = (
                heliotrope.config.MIRRORING_REMOTE_CONCURRENT_SIZE
            )
            mirroring_task.LOCAL_CONCURRENT_SIZE = (
                heliotrope.config.MIRRORING_LOCAL_CONCURRENT_SIZE
            )

            task_manager.register_task(
                mirroring_task.start_mirroring,
                MirroringTask.__name__,
                heliotrope.config.MIRRORING_DELAY,
            )
            task_manager.register_task(
                mirroring_task.start_integrity_check,
                "integrity_check",
                heliotrope.config.INTEGRITY_CHECK_DELAY,
            )


async def closeup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Close session
    await heliotrope.ctx.mongodb.client.close()
    await heliotrope.ctx.sa.engine.dispose()
    await heliotrope.ctx.hitomi_la.session.close()
    heliotrope.shutdown_tasks()


def create_app(config: HeliotropeConfig) -> Heliotrope:
    heliotrope = Heliotrope("heliotrope")
    heliotrope.exception(  # pyright: ignore[reportUnknownMemberType]
        GalleryinfoNotFound, InfoNotFound
    )(not_found)
    heliotrope.config.update(config)
    heliotrope.blueprint(endpoint)
    heliotrope.main_process_start(main_process_startup)
    heliotrope.before_server_start(startup)
    heliotrope.before_server_stop(closeup)

    return heliotrope
