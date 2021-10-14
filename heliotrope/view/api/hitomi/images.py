from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_openapi.openapi3.openapi import summary, tag  # type: ignore

from heliotrope.hitomi.common import image_url_from_image
from heliotrope.hitomi.models import HitomiFiles, HitomiGalleryinfo
from heliotrope.sanic import HeliotropeRequest
from heliotrope.shuffle import shuffle_image_url

hitomi_images = Blueprint("hitomi_images", url_prefix="/images")


class HitomiImagesView(HTTPMethodView):
    @summary("Get hitomi shuffled image url list")  # type: ignore
    @tag("hitomi")  # type: ignore
    async def get(self, request: HeliotropeRequest, index_id: int) -> HTTPResponse:
        galleryinfo = await request.app.ctx.sql_query.get_galleryinfo(
            index_id
        ) or await request.app.ctx.hitomi_request.get_galleyinfo(index_id)

        if isinstance(galleryinfo, HitomiGalleryinfo):
            galleryinfo = galleryinfo.to_dict()

        if not galleryinfo:
            return request.app.ctx.response.not_found

        return json(
            {
                "status": 200,
                "files": [
                    {
                        "name": file.name,
                        "url": shuffle_image_url(
                            image_url_from_image(index_id, file, True)
                        ),
                    }
                    for file in map(HitomiFiles, galleryinfo["files"])
                ],
            }
        )


hitomi_images.add_route(HitomiImagesView.as_view(), "/<index_id:int>")
