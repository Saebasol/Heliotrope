from typing import Optional

from sanic import redirect
from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from heliotrope.infrastructure.sanic.app import HeliotropeRequest

root_endpoint = Blueprint("root", url_prefix="/")


class HeliotropeRootView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest) -> Optional[HTTPResponse]:
        return redirect("/about")


root_endpoint.add_route(HeliotropeRootView.as_view(), "/")
