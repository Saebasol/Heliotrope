from sanic.blueprints import Blueprint

from heliotrope.view.api.hitomi.galleryinfo import hitomi_galleryinfo
from heliotrope.view.api.hitomi.images import hitomi_images
from heliotrope.view.api.hitomi.info import hitomi_info
from heliotrope.view.api.hitomi.list import hitomi_list
from heliotrope.view.api.hitomi.random import hitomi_random
from heliotrope.view.api.hitomi.search import hitomi_search

# NOTE: Will fixed
hitomi_endpoint = Blueprint.group(
    hitomi_galleryinfo,
    hitomi_images,
    hitomi_info,
    hitomi_list,
    hitomi_search,
    hitomi_random,
    url_prefix="/hitomi",
)
