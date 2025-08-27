from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_tags = Blueprint("hitomi_tags", url_prefix="/tags")


class HitomiTagsView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la tags")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="id", location="path", schema=int
    )
    async def get(
        self,
        request: HeliotropeRequest,
    ) -> HTTPResponse:
        return json({})


hitomi_tags.add_route(HitomiTagsView.as_view(), "")
