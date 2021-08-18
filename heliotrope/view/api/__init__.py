from sanic.blueprints import Blueprint

from heliotrope import version_info
from heliotrope.view.api.hitomi import hitomi_endpoint
from heliotrope.view.api.proxy import proxy

# NOTE: Will fixed
api_endpoint = Blueprint.group(
    hitomi_endpoint, proxy, url_prefix="/api", version=version_info.major
)
