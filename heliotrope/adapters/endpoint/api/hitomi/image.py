from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.usecases.get.galleryinfo import GetGalleryinfoUseCase
from heliotrope.application.utils import check_int32
from heliotrope.domain.exceptions import GalleryinfoNotFound
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_image = Blueprint("hitomi_image", url_prefix="/image")


class HitomiImageView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la image")
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

        files = request.app.ctx.javascript_interpreter.image_urls(
            id, galleryinfo.files, False
        )

        return json(
            {
                "files": list(files),
            }
        )


hitomi_image.add_route(HitomiImageView.as_view(), "/<id:int>")
