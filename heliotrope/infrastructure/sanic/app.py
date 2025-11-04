from types import SimpleNamespace
from typing import Any

from sanic.app import Sanic
from sanic.request import Request
from yggdrasil.infrastructure.hitomila import HitomiLa
from yggdrasil.infrastructure.hitomila.repositories.galleryinfo import (
    HitomiLaGalleryinfoRepository,
)
from yggdrasil.infrastructure.mongodb import MongoDB
from yggdrasil.infrastructure.mongodb.repositories.info import MongoDBInfoRepository
from yggdrasil.infrastructure.pythonmonkey.repositories.resolved_image import (
    PythonMonkeyResolvedImageRepository,
)
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)

from heliotrope.application.tasks.mirroring import MirroringTask
from heliotrope.infrastructure.sanic.config import HeliotropeConfig


class HeliotropeContext(SimpleNamespace):
    sa: SQLAlchemy
    hitomi_la: HitomiLa
    mongodb: MongoDB
    sa_galleryinfo_repository: SAGalleryinfoRepository
    hitomi_la_galleryinfo_repository: HitomiLaGalleryinfoRepository
    mongodb_repository: MongoDBInfoRepository
    pythonmonkey_resolved_image_repository: PythonMonkeyResolvedImageRepository
    mirroring_task: MirroringTask


class Heliotrope(Sanic[HeliotropeConfig, HeliotropeContext]): ...


class HeliotropeRequest(Request):
    app: Heliotrope
    args: property
    json: Any
