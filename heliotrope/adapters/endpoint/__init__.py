from sanic.blueprints import Blueprint

from heliotrope.adapters.endpoint.about import about_endpoint
from heliotrope.adapters.endpoint.api import api_endpoint

endpoint = Blueprint.group(api_endpoint, about_endpoint)
