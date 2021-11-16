from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    async def post(self, request) -> HTTPResponse:
        raise NotFound


hitomi_search.add_route(HitomiSearchView.as_view(), "/")
