from sanic.blueprints import Blueprint

from heliotrope.adapters.endpoint.api.hitomi.galleryinfo import hitomi_galleryinfo
from heliotrope.adapters.endpoint.api.hitomi.image import hitomi_image
from heliotrope.adapters.endpoint.api.hitomi.info import hitomi_info
from heliotrope.adapters.endpoint.api.hitomi.list import hitomi_list

hitomi_endpoint = Blueprint.group(
    hitomi_galleryinfo,
    hitomi_image,
    hitomi_info,
    hitomi_list,
    url_prefix="/hitomi",
)
