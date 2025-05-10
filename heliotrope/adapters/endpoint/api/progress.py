from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.infrastructure.sanic.app import HeliotropeRequest

progress_endpoint = Blueprint("progress", url_prefix="/progress")


class MirroringProgressView(HTTPMethodView):
    @openapi.tag("progress")
    @openapi.summary("Get mirroring progress")
    async def get(self, request: HeliotropeRequest) -> HTTPResponse:
        return json(
            request.app.shared_ctx.mirroring_progress_dict.copy(),
            headers={"Access-Control-Allow-Origin": "*"},
        )


progress_endpoint.add_route(MirroringProgressView.as_view(), "/")
