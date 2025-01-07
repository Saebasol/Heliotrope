from sanic.blueprints import Blueprint

from heliotrope.application.api.hitomi.galleryinfo import hitomi_galleryinfo

hitomi_endpoint = Blueprint.group(
    hitomi_galleryinfo,
    url_prefix="/hitomi",
)
