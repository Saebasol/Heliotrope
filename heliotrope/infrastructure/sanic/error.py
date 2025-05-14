from sanic import HTTPResponse, json

from heliotrope.infrastructure.sanic.app import HeliotropeRequest


async def not_found(request: HeliotropeRequest, exception: Exception) -> HTTPResponse:
    return json(
        {
            "message": str(exception),
        },
        status=404,
    )
