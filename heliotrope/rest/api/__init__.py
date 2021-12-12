from sanic.blueprints import Blueprint

from heliotrope.rest.api.hitomi import hitomi_endpoint

api_endpoint = Blueprint.group(hitomi_endpoint, url_prefix="/api")
