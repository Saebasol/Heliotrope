from types import SimpleNamespace
from typing import Any

from sanic.app import Sanic
from sanic.request import Request

from heliotrope.application.config import HeliotropeConfig
from heliotrope.application.javascript.interpreter import JavaScriptInterpreter
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.hitomila.galleryinfo.domain.repository import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.sqlalchemy import SQLAlchemy
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.repository import (
    SAGalleryinfoRepository,
)


class HeliotropeContext(SimpleNamespace):
    sa: SQLAlchemy
    hitomi_la: HitomiLa
    sa_galleryinfo_repository: SAGalleryinfoRepository
    hitomi_la_galleryinfo_repository: HitomiLaGalleryinfoRepository
    javascript_interpreter: JavaScriptInterpreter


class Heliotrope(Sanic[HeliotropeConfig, HeliotropeContext]): ...


class HeliotropeRequest(Request):
    app: Heliotrope
    args: property
    json: Any
