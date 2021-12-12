from types import SimpleNamespace
from typing import Any

from sanic.app import Sanic
from sanic.request import Request

from heliotrope.config import HeliotropeConfig
from heliotrope.database.meilisearch.client import MeiliSearch
from heliotrope.database.orm import ORM
from heliotrope.interpreter import CommonJS
from heliotrope.request.base import BaseRequest
from heliotrope.request.hitomi import HitomiRequest


class HeliotropeContext(SimpleNamespace):
    orm: ORM
    meilisearch: MeiliSearch
    request: BaseRequest
    hitomi_request: HitomiRequest
    common_js: CommonJS


class Heliotrope(Sanic):
    ctx: HeliotropeContext
    config: HeliotropeConfig


class HeliotropeRequest(Request):
    app: Heliotrope
    args: property
    json: Any
