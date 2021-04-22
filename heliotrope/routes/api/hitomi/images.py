from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import get_galleryinfo
from heliotrope.utils.hitomi.common import image_url_from_image
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel, HitomiImageModel
from heliotrope.utils.response import not_found
from heliotrope.utils.shuffle import shuffle_image_url
from heliotrope.utils.typed import HeliotropeRequest

hitomi_images = Blueprint("hitomi_images", url_prefix="/images")


class HitomiImagesInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index):
        if query_galleryinfo := await get_galleryinfo(index):
            files = HitomiImageModel.image_model_generator(query_galleryinfo["files"])
        elif requested_galleryinfo := await request.app.ctx.hitomi_requester.get_galleryinfo(
            index
        ):
            files = HitomiImageModel.image_model_generator(requested_galleryinfo.files)
        else:
            return not_found
        return json(
            {
                "files": list(
                    map(
                        lambda file: {
                            "name": file.name,
                            "image": shuffle_image_url(
                                image_url_from_image(int(index), file, True)
                            ),
                        },
                        files,
                    )
                )
            }
        )


hitomi_images.add_route(HitomiImagesInfoView.as_view(), "/<index:int>")
