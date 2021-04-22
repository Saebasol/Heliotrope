from sanic.response import json

not_found = json({"status": 404, "message": "not_found"}, 404)

bad_request = json({"status": 400, "message": "bad_request"}, 400)

forbidden = json({"status": 403, "message": "not_authorized"}, 403)
