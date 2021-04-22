from sanic.blueprints import Blueprint

from heliotrope.routes.api.hitomi.galleryinfo import hitomi_galleyinfo
from heliotrope.routes.api.hitomi.images import hitomi_images
from heliotrope.routes.api.hitomi.info import hitomi_info
from heliotrope.routes.api.hitomi.list import hitomi_list
from heliotrope.routes.api.hitomi.search import hitomi_search

hitomi_endpoint = Blueprint.group(
    hitomi_galleyinfo,
    hitomi_images,
    hitomi_info,
    hitomi_list,
    hitomi_search,
    url_prefix="/hitomi",
)
