from sanic.blueprints import Blueprint

from heliotrope.rest.api.hitomi.galleryinfo import hitomi_galleryinfo
from heliotrope.rest.api.hitomi.info import hitomi_info
from heliotrope.rest.api.hitomi.list import hitomi_list
from heliotrope.rest.api.hitomi.random import hitomi_random
from heliotrope.rest.api.hitomi.search import hitomi_search

hitomi_endpoint = Blueprint.group(
    hitomi_search,
    hitomi_galleryinfo,
    hitomi_info,
    hitomi_list,
    hitomi_random,
    url_prefix="/hitomi",
)
