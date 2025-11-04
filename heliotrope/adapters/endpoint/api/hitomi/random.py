from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.types import Schema
from yggdrasil.application.dtos.search import PostSearchBodyDTO
from yggdrasil.application.usecases.get.info import GetRandomInfoUseCase

from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_random = Blueprint("hitomi_random", url_prefix="/random")


class HitomiRandomView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get random result in hitomi")
    @openapi.body(  # pyright: ignore[reportUnknownMemberType]
        {
            "application/json": openapi.Object(
                {
                    "query": Schema.make(value=["language:korean"]),  # type: ignore
                }
            )
        }
    )
    @validate(json=PostSearchBodyDTO, body_argument="body")
    async def post(
        self, request: HeliotropeRequest, body: PostSearchBodyDTO
    ) -> HTTPResponse:
        info = await GetRandomInfoUseCase(request.app.ctx.mongodb_repository).execute(
            body.query
        )

        return json(info.to_dict())


hitomi_random.add_route(HitomiRandomView.as_view(), "/")
