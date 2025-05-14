from sanic import json

from heliotrope.infrastructure.sanic.app import HeliotropeRequest


async def not_found(request: HeliotropeRequest, exception: Exception):
    return json(
        {
            "message": str(exception),
        },
        status=404,
    )
