from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_openapi.openapi3.openapi import summary, tag  # type: ignore

from heliotrope.sanic import HeliotropeRequest

hitomi_random = Blueprint("hitomi_random", url_prefix="/random")


class HitomiInfoView(HTTPMethodView):
    @summary("Get random result in hitomi")  # type: ignore
    @tag("hitomi")  # type: ignore
    async def get(self, request: HeliotropeRequest) -> HTTPResponse:
        info = await request.app.ctx.nosql_query.find_random_info()
        return json({"status": 200, **info})


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_random.add_route(HitomiInfoView.as_view(), "")  # type: ignore
