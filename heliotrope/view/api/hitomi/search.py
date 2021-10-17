from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_openapi.openapi3.openapi import body, summary, tag  # type: ignore
from sanic_openapi.openapi3.types import Integer, Object, Schema  # type: ignore

from heliotrope.sanic import HeliotropeRequest

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    @summary("Get search result in hitomi")  # type: ignore
    @tag("hitomi")  # type: ignore
    @body(
        {
            "application/json": Object(
                {
                    "offset": Integer(default=1),
                    "query": Schema.make(value=["sekigahara", "artist:tsukako"]),  # type: ignore
                }
            )
        },
        description="This is the request body for the search.",
        required=True,
    )
    async def post(self, request: HeliotropeRequest) -> HTTPResponse:
        offset = (
            int(offset) - 1
            if (offset := request.json.get("offset")) and not (int(offset) - 1 < 0)
            else 0
        )

        if (
            (query := request.json.get("query"))
            and query
            and (
                search_result := await request.app.ctx.nosql_query.search_info_list(
                    query, offset
                )
            )
        ):
            result, count = search_result
            return json(
                {
                    "status": 200,
                    "result": result,
                    "count": count,
                }
            )

        return request.app.ctx.response.not_found


hitomi_search.add_route(HitomiSearchView.as_view(), "")
