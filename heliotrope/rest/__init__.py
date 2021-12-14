from sanic.blueprints import Blueprint

from heliotrope.rest.api import api_endpoint

# NOTE: Will fixed
rest = Blueprint.group(api_endpoint)
