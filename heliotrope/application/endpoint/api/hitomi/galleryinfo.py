from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.sanic import HeliotropeRequest

from heliotrope.core.galleryinfo.usecases.get import GetGalleryinfoUseCase

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryinfoView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la galleryinfo")
    @openapi.parameter(name="id", location="path", schema=int)
    async def get(
        self,
        request: HeliotropeRequest,
        id: int,
    ) -> HTTPResponse:
        galleryinfo = await GetGalleryinfoUseCase(
            request.app.ctx.hitomi_la_galleryinfo_repository
        ).execute(id) or await GetGalleryinfoUseCase(
            request.app.ctx.sa_galleryinfo_repository
        ).execute(
            id
        )

        return json(galleryinfo.to_dict())


hitomi_galleryinfo.add_route(HitomiGalleryinfoView.as_view(), "/<id:int>")
