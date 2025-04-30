from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.types import Schema

from heliotrope.application.usecases.get.info import GetRandomInfoUseCase
from heliotrope.infrastructure.sanic import HeliotropeRequest

hitomi_random = Blueprint("hitomi_random", url_prefix="/random")


class HitomiRandomView(HTTPMethodView):
    @openapi.summary("Get random result in hitomi")
    @openapi.tag("hitomi")
    @openapi.body(  # pyright: ignore[reportUnknownMemberType]
        {
            "application/json": openapi.Object(
                {
                    "query": Schema.make(value=["language:korean"]),  # type: ignore
                }
            )
        }
    )
    async def post(self, request: HeliotropeRequest) -> HTTPResponse:
        query: list[str] = request.json.get("query") if request.json else []
        info = await GetRandomInfoUseCase(request.app.ctx.mongodb_repository).execute(
            query
        )

        return json(
            {
                "status": 200,
                **request.app.ctx.javascript_interpreter.convert_thumbnail(info),
            }
        )


hitomi_random.add_route(HitomiRandomView.as_view(), "/")
