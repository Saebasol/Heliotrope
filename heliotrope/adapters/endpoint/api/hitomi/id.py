from gzip import compress
from struct import pack

from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, raw
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.usecases.get.galleryinfo import GetAllGalleryinfoIdsUseCase
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_id = Blueprint("hitomi_id", url_prefix="/id")


class HitomiGalleryinfoView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la all galleryinfo id")
    async def get(
        self,
        request: HeliotropeRequest,
    ) -> HTTPResponse:
        ids = await GetAllGalleryinfoIdsUseCase(
            request.app.ctx.sa_galleryinfo_repository
        ).execute()

        return raw(
            compress(pack(f"<{len(ids)}I", *ids)), headers={"Content-Encoding": "gzip"}
        )


hitomi_id.add_route(HitomiGalleryinfoView.as_view(), "")
