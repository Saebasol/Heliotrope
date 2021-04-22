from sanic import Blueprint
from sanic.views import HTTPMethodView

from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")
from sanic.response import json


class HitomiInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int):
        if tags_dict := await request.app.ctx.hitomi_requester.get_info_using_index(
            index
        ):
            return json({"status": 200, **tags_dict})

        return not_found


hitomi_info.add_route(HitomiInfoView.as_view(), "/<index:int>")
