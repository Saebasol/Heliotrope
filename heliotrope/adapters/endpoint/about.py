from typing import Optional

from sanic import file
from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from heliotrope.infrastructure.sanic.app import HeliotropeRequest

about_endpoint = Blueprint("about", url_prefix="/about")


class HeliotropeAboutView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest) -> Optional[HTTPResponse]:
        return await file(
            "./heliotrope/adapters/endpoint/about.html",
            mime_type="text/html",
        )


about_endpoint.add_route(HeliotropeAboutView.as_view(), "/")
