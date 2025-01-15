from sanic.blueprints import Blueprint

from heliotrope.application.api.hitomi import hitomi_endpoint
from heliotrope.application.api.proxy import proxy_endpoint

api_endpoint = Blueprint.group(hitomi_endpoint, proxy_endpoint, url_prefix="/api")
