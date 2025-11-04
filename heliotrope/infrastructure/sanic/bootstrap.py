from asyncio import AbstractEventLoop
from multiprocessing import Lock, Manager

from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration
from yggdrasil.domain.exceptions import GalleryinfoNotFound, InfoNotFound
from yggdrasil.infrastructure.hitomila import HitomiLa
from yggdrasil.infrastructure.hitomila.repositories.galleryinfo import (
    HitomiLaGalleryinfoRepository,
)
from yggdrasil.infrastructure.mongodb import MongoDB
from yggdrasil.infrastructure.mongodb.repositories.info import MongoDBInfoRepository
from yggdrasil.infrastructure.pythonmonkey import JavaScriptInterpreter
from yggdrasil.infrastructure.pythonmonkey.repositories.resolved_image import (
    PythonMonkeyResolvedImageRepository,
)
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.character import (
    SACharacterRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.group import SAGroupRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.language_localname import (
    SALanguageLocalnameRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.tag import SATagRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.type import SATypeRepository

from heliotrope import __version__
from heliotrope.adapters.endpoint import endpoint
from heliotrope.application.tasks.manager import TaskManager
from heliotrope.application.tasks.refresh import RefreshggJS
from heliotrope.infrastructure.sanic.app import Heliotrope
from heliotrope.infrastructure.sanic.config import HeliotropeConfig
from heliotrope.infrastructure.sanic.error import not_found


async def main_process_startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    manager = Manager()
    heliotrope.shared_ctx.namespace = manager.Namespace()
    heliotrope.shared_ctx.namespace.is_running_first_process = False


async def startup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    if heliotrope.config.PRODUCTION:  # pragma: no cover
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
    heliotrope.ctx.hitomi_la = await HitomiLa.create([])
    heliotrope.ctx.mongodb = await MongoDB.create(heliotrope.config.INFO_DB_URL)

    heliotrope.ctx.hitomi_la_galleryinfo_repository = HitomiLaGalleryinfoRepository(
        heliotrope.ctx.hitomi_la
    )
    heliotrope.ctx.sa_galleryinfo_repository = SAGalleryinfoRepository(
        heliotrope.ctx.sa,
        SATypeRepository(heliotrope.ctx.sa),
        SAArtistRepository(heliotrope.ctx.sa),
        SALanguageInfoRepository(heliotrope.ctx.sa),
        SALanguageLocalnameRepository(heliotrope.ctx.sa),
        SACharacterRepository(heliotrope.ctx.sa),
        SAGroupRepository(heliotrope.ctx.sa),
        SAParodyRepository(heliotrope.ctx.sa),
        SATagRepository(heliotrope.ctx.sa),
    )
    heliotrope.ctx.mongodb_repository = MongoDBInfoRepository(
        heliotrope.ctx.mongodb, heliotrope.config.USE_ATLAS_SEARCH
    )

    heliotrope.ctx.pythonmonkey_resolved_image_repository = (
        PythonMonkeyResolvedImageRepository(
            await JavaScriptInterpreter.setup(heliotrope.ctx.hitomi_la)
        )
    )

    refresh_gg_js = RefreshggJS(heliotrope)
    task_manager = TaskManager(heliotrope)

    if not heliotrope.test_mode:  # pragma: no cover
        task_manager.register_task(
            refresh_gg_js.start,
            RefreshggJS.__name__,
            heliotrope.config.REFRESH_GG_JS_DELAY,
        )

    with Lock():
        namespace = heliotrope.shared_ctx.namespace

        if not namespace.is_running_first_process:
            namespace.is_running_first_process = True
            await heliotrope.ctx.sa.create_all_table()
            await heliotrope.ctx.mongodb.collection.create_index([("id", -1)])
            if (
                heliotrope.ctx.mongodb.is_atlas and heliotrope.config.USE_ATLAS_SEARCH
            ):  # pragma: no cover
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


async def closeup(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    # Close session
    await heliotrope.ctx.mongodb.client.close()
    await heliotrope.ctx.sa.engine.dispose()
    await heliotrope.ctx.hitomi_la.session.close()
    for task in heliotrope.tasks:
        await heliotrope.cancel_task(task.get_name())


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
