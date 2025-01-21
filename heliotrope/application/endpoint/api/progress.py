from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.sanic import HeliotropeRequest


progress_endpoint = Blueprint("progress", url_prefix="/progress")


class MirroringProgressView(HTTPMethodView):
    @openapi.tag("progress")
    @openapi.summary("Get mirroring progress")
    async def get(self, request: HeliotropeRequest) -> HTTPResponse:
        progress = request.app.ctx.mirroring_task.progress
        return json(
            progress.to_dict(),
            headers={"Access-Control-Allow-Origin": "*"},
        )


progress_endpoint.add_route(MirroringProgressView.as_view(), "/")
