from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

hitomi_random = Blueprint("hitomi_random", url_prefix="/random")


class HitomiRandomView(HTTPMethodView):
    async def get(self, request) -> HTTPResponse:
        raise NotFound


hitomi_random.add_route(HitomiRandomView.as_view(), "/")
