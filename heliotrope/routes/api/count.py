from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import add_request_count, get_all_request_count
from heliotrope.utils.decorators import hiyobot_only
from heliotrope.utils.response import bad_request, not_found
from heliotrope.utils.typed import HeliotropeRequest

heliotrope_request_count = Blueprint("request_count", url_prefix="/count")


class HeliotropeRequestCountView(HTTPMethodView):
    @hiyobot_only
    async def get(self, request):
        if ranking := await get_all_request_count():
            ranking.update({"status": 200})
            return json(ranking)
        return not_found

    @hiyobot_only
    async def post(self, request: HeliotropeRequest):
        if index := request.json.get("index"):
            if await add_request_count(index):
                return json({"status": 200})
        return bad_request


heliotrope_request_count.add_route(HeliotropeRequestCountView.as_view(), "")
