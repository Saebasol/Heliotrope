from asyncio.tasks import gather

from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import get_galleryinfo, get_sorted_index
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest
from heliotrope.utils.useful import is_raw, parse_raw_galleryinfo_list

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int):
        hitomi_index_list = await get_sorted_index()
        split_hitomi_index_list = list(
            map(
                lambda i: hitomi_index_list[i * 15 : (i + 1) * 15],
                range((len(hitomi_index_list) + 15 - 1) // 15),
            )
        )

        start_at_zero = index - 1

        if len(split_hitomi_index_list) < start_at_zero + 1 or start_at_zero < 0:
            return not_found

        info_list = await gather(
            *[
                get_galleryinfo(index, include_files=False)
                for index in split_hitomi_index_list[start_at_zero]
            ]
        )

        if is_raw(request.args):
            return json({"status": 200, "list": info_list})

        return json(
            {
                "status": 200,
                "list": parse_raw_galleryinfo_list(info_list, include_files=False),
            }
        )


hitomi_list.add_route(HitomiListView.as_view(), "/<index:int>")
