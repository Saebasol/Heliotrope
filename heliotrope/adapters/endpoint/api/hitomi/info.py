from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.usecases.get.galleryinfo import GetGalleryinfoUseCase
from heliotrope.application.usecases.get.info import GetInfoUseCase
from heliotrope.application.utils import check_int64
from heliotrope.domain.entities.info import Info
from heliotrope.domain.exceptions import GalleryinfoNotFound, InfoNotFound
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")


class HitomiInfoView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi info")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="id", location="path", schema=int
    )
    async def get(self, request: HeliotropeRequest, id: int) -> HTTPResponse:
        check_int64(id)
        try:
            info = await GetInfoUseCase(request.app.ctx.mongodb_repository).execute(id)
        except InfoNotFound:
            try:
                galleryinfo = await GetGalleryinfoUseCase(
                    request.app.ctx.hitomi_la_galleryinfo_repository
                ).execute(id)
                info = Info.from_galleryinfo(galleryinfo)
            except GalleryinfoNotFound:
                raise InfoNotFound(str(id))

        return json(
            {
                **request.app.ctx.javascript_interpreter.convert_thumbnail(info),
            }
        )


hitomi_info.add_route(HitomiInfoView.as_view(), "/<id:int>")
