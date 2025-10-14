from sanic.blueprints import Blueprint

from heliotrope.adapters.endpoint.api import api_endpoint
from heliotrope.adapters.endpoint.root import root_endpoint

endpoint = Blueprint.group(api_endpoint, root_endpoint)
