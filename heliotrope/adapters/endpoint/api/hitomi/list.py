from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.usecases.get.info import (
    GetAllInfoIdsUseCase,
    GetListInfoUseCase,
)
from heliotrope.application.utils import check_int64
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get latest hitomi info list")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="index", location="path", schema=int
    )
    async def get(self, request: HeliotropeRequest, index: int) -> HTTPResponse:
        check_int64(index)
        total = len(await GetAllInfoIdsUseCase(request.app.ctx.mongodb_repository))

        start_at_zero = index - 1

        if start_at_zero < 0 or total < start_at_zero:
            raise InvalidUsage

        info_list = await GetListInfoUseCase(
            request.app.ctx.mongodb_repository
        ).execute(start_at_zero, 15)

        return json(
            {
                "list": [info.to_dict() for info in info_list],
                "total": total,
            }
        )


hitomi_list.add_route(HitomiListView.as_view(), "/<index:int>")
