from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi.openapi import summary, tag  # type: ignore

from heliotrope.sanic import HeliotropeRequest

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")


class HitomiInfoView(HTTPMethodView):
    @summary("Get hitomi info")  # type: ignore
    @tag("hitomi")  # type: ignore
    async def get(self, request: HeliotropeRequest, index_id: int) -> HTTPResponse:
        if info := await request.app.ctx.nosql_query.find_info(index_id):
            return json({"status": 200, **info})

        if requested_info := await request.app.ctx.hitomi_request.get_info(index_id):
            return json({"status": 200, **requested_info.to_dict()})

        return request.app.ctx.response.not_found


hitomi_info.add_route(HitomiInfoView.as_view(), "/<index_id:int>")
