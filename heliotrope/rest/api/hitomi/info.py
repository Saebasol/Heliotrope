from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

hitomi_info = Blueprint("hitomi_info", url_prefix="/info")


class HitomiInfoView(HTTPMethodView):
    async def get(self, request) -> HTTPResponse:
        raise NotFound


hitomi_info.add_route(HitomiInfoView.as_view(), "/")
