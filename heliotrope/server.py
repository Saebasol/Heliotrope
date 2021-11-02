from asyncio.events import AbstractEventLoop
from asyncio.tasks import create_task
from os import environ, getenv

from aiohttp.client import ClientSession
from sanic.app import Sanic
from sanic_openapi import openapi3_blueprint  # type: ignore
from sentry_sdk import init
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise import Tortoise

from heliotrope import __version__
from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.request.base import BaseRequest
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.response import Response
from heliotrope.sanic import Heliotrope
from heliotrope.tasks.mirroring import Mirroring
from heliotrope.tasks.refresh import RefreshCommonJS
from heliotrope.view import view

heliotrope = Sanic("heliotrope")

# NOTE: Will fixed
heliotrope.blueprint(view)
heliotrope.blueprint(openapi3_blueprint)

# TODO: Type hint
@heliotrope.main_process_start
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    heliotrope.config.API_VERSION = __version__
    heliotrope.config.API_TITLE = "Heliotrope"
    heliotrope.config.API_DESCRIPTION = "Hitomi.la mirror api"
    heliotrope.config.API_LICENSE_NAME = "MIT"

    if not heliotrope.config.TESTING:
        init(
            dsn=environ["SENTRY_DSN"],
            integrations=[SanicIntegration()],
            release=f"heliotrope@{__version__}",
        )
        heliotrope.config.FORWARDED_SECRET = environ["FORWARDED_SECRET"]
        heliotrope.config.API_SCHEMES = ["https"]

    await Tortoise.init(
        db_url=heliotrope.config.DB_URL,
        modules={"models": ["heliotrope.database.models.hitomi"]},
    )
    await Tortoise.generate_schemas()
    heliotrope.config.FALLBACK_ERROR_FORMAT = "json"
    heliotrope.ctx.sql_query = SQLQuery()
    heliotrope.ctx.nosql_query = NoSQLQuery(heliotrope.config.MONGO_DB_URL)
    heliotrope.ctx.response = Response()
    heliotrope.ctx.base_request = BaseRequest(ClientSession())
    heliotrope.ctx.hitomi_request = await HitomiRequest.setup(
        index_file=heliotrope.config.INDEX_FILE
    )
    heliotrope.ctx.mirroring = await Mirroring.setup(
        sql_query=heliotrope.ctx.sql_query,
        nosql_query=heliotrope.ctx.nosql_query,
    )
    heliotrope.ctx.mirroring_task = create_task(
        heliotrope.ctx.mirroring.task(heliotrope.config.DELAY)
    )
    heliotrope.ctx.refresh_common_js = RefreshCommonJS(
        heliotrope.ctx.hitomi_request.get_common_js
    )
    heliotrope.ctx.common_js_refresh_task = create_task(
        heliotrope.ctx.refresh_common_js.task(heliotrope.config.REFRESH_DELAY)
    )


# TODO: Type hint
@heliotrope.main_process_stop
async def stop(heliotrope: Heliotrope, loop: AbstractEventLoop) -> None:
    await Tortoise.close_connections()
    heliotrope.ctx.nosql_query.close()
    await heliotrope.ctx.base_request.close()
    await heliotrope.ctx.hitomi_request.close()
    await heliotrope.ctx.mirroring.close()
    heliotrope.ctx.mirroring_task.cancel()
