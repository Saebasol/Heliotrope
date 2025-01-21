from sanic.blueprints import Blueprint

from heliotrope.application.endpoint.api.hitomi import hitomi_endpoint
from heliotrope.application.endpoint.api.proxy import proxy_endpoint
from heliotrope.application.endpoint.api.progress import progress_endpoint


api_endpoint = Blueprint.group(
    hitomi_endpoint,
    proxy_endpoint,
    progress_endpoint,
    url_prefix="/api",
)
