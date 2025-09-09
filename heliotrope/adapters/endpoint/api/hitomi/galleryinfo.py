from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.usecases.get.galleryinfo import GetGalleryinfoUseCase
from heliotrope.application.utils import check_int32
from heliotrope.domain.entities.raw_galleryinfo import RawGalleryinfo
from heliotrope.domain.exceptions import GalleryinfoNotFound
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryinfoView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la galleryinfo")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="id", location="path", schema=int
    )
    async def get(
        self,
        request: HeliotropeRequest,
        id: int,
    ) -> HTTPResponse:
        check_int32(id)
        try:
            galleryinfo = await GetGalleryinfoUseCase(
                request.app.ctx.sa_galleryinfo_repository
            ).execute(id)
        except GalleryinfoNotFound:
            galleryinfo = await GetGalleryinfoUseCase(
                request.app.ctx.hitomi_la_galleryinfo_repository
            ).execute(id)

        return json(RawGalleryinfo.from_galleryinfo(galleryinfo).to_dict())


hitomi_galleryinfo.add_route(HitomiGalleryinfoView.as_view(), "/<id:int>")
