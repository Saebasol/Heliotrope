from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi
from yggdrasil.application.usecases.get.galleryinfo import GetGalleryinfoUseCase
from yggdrasil.application.usecases.get.resolved_image import GetResolvedImageUseCase
from yggdrasil.domain.exceptions import GalleryinfoNotFound

from heliotrope.application.utils import check_int32
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

        return json(
            [
                GetResolvedImageUseCase(
                    request.app.ctx.pythonmonkey_resolved_image_repository
                )
                .execute(galleryinfo.id, file)
                .to_dict()
                for file in galleryinfo.files
            ]
        )


hitomi_image.add_route(HitomiImageView.as_view(), "/<id:int>")
