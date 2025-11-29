from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.types import Schema
from yggdrasil.application.dtos.search import (
    PostSearchBodyDTO,
    PostSearchQueryDTO,
    SearchResultDTO,
)
from yggdrasil.application.usecases.get.info import SearchByQueryUseCase

from heliotrope.application.utils import check_int32
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get search result in hitomi")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="offset",
        location="query",
        schema=Schema.make(  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
            int, default=1
        ),
        required=True,
    )
    @openapi.body(  # pyright: ignore[reportUnknownMemberType]
        {
            "application/json": openapi.Object(
                {
                    "query": Schema.make(value=["sekigahara", "artist:tsukako"]),  # type: ignore
                }
            )
        }
    )
    @validate(
        json=PostSearchBodyDTO,
        query=PostSearchQueryDTO,
        query_argument="query",
        body_argument="body",
    )
    async def post(
        self,
        request: HeliotropeRequest,
        body: PostSearchBodyDTO,
        query: PostSearchQueryDTO,
    ) -> HTTPResponse:
        check_int32(query.offset)
        offset = 0 if query.offset - 1 < 0 else query.offset - 1
        check_int32(offset)
        if body.query and any(q for q in body.query):
            count, results = await SearchByQueryUseCase(
                request.app.ctx.mongodb_repository
            ).execute(body.query, offset)
            return json(SearchResultDTO(results=results, count=count).to_dict())

        raise InvalidUsage


hitomi_search.add_route(HitomiSearchView.as_view(), "/")
