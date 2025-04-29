from sanic.blueprints import Blueprint

from heliotrope.adapters.endpoint.api.hitomi import hitomi_endpoint
from heliotrope.adapters.endpoint.api.progress import progress_endpoint
from heliotrope.adapters.endpoint.api.proxy import proxy_endpoint

api_endpoint = Blueprint.group(
    hitomi_endpoint,
    proxy_endpoint,
    progress_endpoint,
    url_prefix="/api",
)
