from sanic.blueprints import Blueprint

from heliotrope.view.api import api_endpoint

# NOTE: Will fixed
view = Blueprint.group(api_endpoint)
