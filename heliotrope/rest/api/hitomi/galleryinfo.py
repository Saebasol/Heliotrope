from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryinfoView(HTTPMethodView):
    async def get(self, request) -> HTTPResponse:
        raise NotFound


hitomi_galleryinfo.add_route(HitomiGalleryinfoView.as_view(), "/")
