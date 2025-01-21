from types import SimpleNamespace
from typing import Any

from sanic.app import Sanic
from sanic.request import Request

from heliotrope.application.config import HeliotropeConfig
from heliotrope.application.javascript.interpreter import JavaScriptInterpreter
from heliotrope.application.tasks.mirroring import MirroringTask
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.hitomila.galleryinfo.domain.repository import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.mongodb.info import MongoDB
from heliotrope.infrastructure.mongodb.info.domain.repository import (
    MongoDBInfoRepository,
)
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.repository import (
    SAGalleryinfoRepository,
)


class HeliotropeContext(SimpleNamespace):
    sa: SQLAlchemy
    hitomi_la: HitomiLa
    mongodb: MongoDB
    sa_galleryinfo_repository: SAGalleryinfoRepository
    hitomi_la_galleryinfo_repository: HitomiLaGalleryinfoRepository
    mongodb_repository: MongoDBInfoRepository
    javascript_interpreter: JavaScriptInterpreter
    mirroring_task: MirroringTask


class Heliotrope(Sanic[HeliotropeConfig, HeliotropeContext]): ...


class HeliotropeRequest(Request):
    app: Heliotrope
    args: property
    json: Any
