from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.exceptions import GalleryinfoNotFound, InfoNotFound
from heliotrope.application.usecases.get.galleryinfo import GetGalleryinfoUseCase
from heliotrope.application.usecases.get.info import GetInfoUseCase
from heliotrope.domain.entities.info import Info
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")


class HitomiInfoView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi info")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="id", location="path", schema=int
    )
    async def get(self, request: HeliotropeRequest, id: int) -> HTTPResponse:
        try:
            info = await GetInfoUseCase(request.app.ctx.mongodb_repository).execute(id)
        except InfoNotFound:
            try:
                galleryinfo = await GetGalleryinfoUseCase(
                    request.app.ctx.sa_galleryinfo_repository
                ).execute(id)
                info = Info.from_galleryinfo(galleryinfo)
            except GalleryinfoNotFound:
                raise InfoNotFound

        return json(
            {
                "status": 200,
                **request.app.ctx.javascript_interpreter.convert_thumbnail(info),
            }
        )


hitomi_info.add_route(HitomiInfoView.as_view(), "/<id:int>")
