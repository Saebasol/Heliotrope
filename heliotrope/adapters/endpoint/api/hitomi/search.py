from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.types import Schema

from heliotrope.application.usecases.get.info import SearchByQueryUseCase
from heliotrope.application.utils import check_int32
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get search result in hitomi")
    @openapi.body(  # pyright: ignore[reportUnknownMemberType]
        {
            "application/json": openapi.Object(
                {
                    "offset": openapi.Integer(default=1),  # type: ignore
                    "query": Schema.make(value=["sekigahara", "artist:tsukako"]),  # type: ignore
                }
            )
        }
    )
    async def post(self, request: HeliotropeRequest) -> HTTPResponse:
        offset = (
            int(offset) - 1
            if (offset := request.json.get("offset")) and not (int(offset) - 1 < 0)
            else 0
        )
        check_int32(offset)
        if (query := request.json.get("query")) and query and any(q for q in query):
            count, results = await SearchByQueryUseCase(
                request.app.ctx.mongodb_repository
            ).execute(query, offset)
            return json(
                {
                    "status": 200,
                    "result": [
                        request.app.ctx.javascript_interpreter.convert_thumbnail(result)
                        for result in results
                    ],
                    "count": count,
                }
            )
        raise InvalidUsage


hitomi_search.add_route(HitomiSearchView.as_view(), "/")
