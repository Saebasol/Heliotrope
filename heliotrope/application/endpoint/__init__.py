from sanic.blueprints import Blueprint

from heliotrope.application.endpoint.api import api_endpoint
from heliotrope.application.endpoint.about import about_endpoint

endpoint = Blueprint.group(api_endpoint, about_endpoint)
