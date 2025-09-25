from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.infrastructure.sanic.app import HeliotropeRequest

status_endpoint = Blueprint("status", url_prefix="/status")


class MirroringStatusView(HTTPMethodView):
    @openapi.tag("status")
    @openapi.summary("Get mirroring status")
    async def get(self, request: HeliotropeRequest) -> HTTPResponse:
        return json(
            request.app.shared_ctx.mirroring_status_dict.copy(),
            headers={"Access-Control-Allow-Origin": "*"},
        )


status_endpoint.add_route(MirroringStatusView.as_view(), "/")
