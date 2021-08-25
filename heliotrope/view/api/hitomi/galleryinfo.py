from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_openapi.openapi3.openapi import summary, tag  # type: ignore

from heliotrope.sanic import HeliotropeRequest

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryinfoView(HTTPMethodView):
    @summary("Get hitomi galleryinfo")  # type: ignore
    @tag("hitomi")  # type: ignore
    async def get(self, request: HeliotropeRequest, index_id: int) -> HTTPResponse:
        if galleryinfo := await request.app.ctx.sql_query.get_galleryinfo(index_id):
            return json({"status": 200, **galleryinfo})

        if requested_galleryinfo := await request.app.ctx.hitomi_request.get_galleyinfo(
            index_id
        ):
            return json({"status": 200, **requested_galleryinfo.to_dict()})

        return request.app.ctx.response.not_found


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_galleryinfo.add_route(HitomiGalleryinfoView.as_view(), "/<index_id:int>")  # type: ignore
