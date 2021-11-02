from asyncio.tasks import Task
from types import SimpleNamespace
from typing import Any, NoReturn

from sanic.app import Sanic
from sanic.config import Config
from sanic.request import Request

from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.request.base import BaseRequest
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.response import Response
from heliotrope.tasks.mirroring import Mirroring
from heliotrope.tasks.refresh import RefreshCommonJS


class HeliotropeContext(SimpleNamespace):
    sql_query: SQLQuery
    nosql_query: NoSQLQuery
    response: Response
    hitomi_request: HitomiRequest
    base_request: BaseRequest
    mirroring: Mirroring
    mirroring_task: Task[NoReturn]
    refresh_common_js: RefreshCommonJS
    refresh_common_js_task: Task[NoReturn]


class HeliotropeConfig(Config):
    INDEX_FILE: str
    DELAY: int
    REFRESH_DELAY: int
    MONGO_DB_URL: str
    DB_URL: str
    TESTING: bool


class Heliotrope(Sanic):
    ctx: HeliotropeContext
    config: HeliotropeConfig


class HeliotropeRequest(Request):
    app: Heliotrope
    args: property
    json: Any
