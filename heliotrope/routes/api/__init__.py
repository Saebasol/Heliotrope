from sanic.blueprints import Blueprint

from heliotrope import version_info
from heliotrope.routes.api.count import heliotrope_request_count
from heliotrope.routes.api.hitomi import hitomi_endpoint
from heliotrope.routes.api.proxy import heliotrope_image_proxy

heliotrope_api = Blueprint.group(
    hitomi_endpoint,
    heliotrope_request_count,
    heliotrope_image_proxy,
    url_prefix="/api",
    version=f"v{version_info.major}",
)
