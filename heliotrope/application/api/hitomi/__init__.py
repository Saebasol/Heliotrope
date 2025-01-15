from sanic.blueprints import Blueprint

from heliotrope.application.api.hitomi.galleryinfo import hitomi_galleryinfo
from heliotrope.application.api.hitomi.image import hitomi_image

hitomi_endpoint = Blueprint.group(
    hitomi_galleryinfo,
    hitomi_image,
    url_prefix="/hitomi",
)
