from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from heliotrope.sanic import HeliotropeRequest

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int) -> HTTPResponse:
        total = request.app.ctx.mirroring.total // 15

        start_at_zero = index - 1

        if start_at_zero < 0 or total < start_at_zero:
            return request.app.ctx.response.bad_request

        info_list = await request.app.ctx.nosql_query.get_info_list(start_at_zero)

        return json({"status": 200, "list": info_list, "total": total})


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
hitomi_list.add_route(HitomiListView.as_view(), "/<index:int>")  # type: ignore
