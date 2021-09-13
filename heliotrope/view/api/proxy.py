from typing import Optional

from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from heliotrope.sanic import HeliotropeRequest
from heliotrope.shuffle import solve_shuffle_image_url

proxy = Blueprint("proxy", url_prefix="/proxy")


class HeliotropeImageProxyView(HTTPMethodView):
    async def get(
        self, request: HeliotropeRequest, shuffled_image_url: str
    ) -> Optional[HTTPResponse]:
        if url := solve_shuffle_image_url(shuffled_image_url):
            headers = request.app.ctx.hitomi_request.headers

            if "pximg" in url:
                headers.update({"referer": "https://pixiv.net"})

            async with request.app.ctx.base_request.session.get(
                url, headers=headers
            ) as request_response:

                if request_response.status != 200:
                    return request.app.ctx.response.bad_request

                response: HTTPResponse = await request.respond(
                    content_type=request_response.content_type
                )

                async for data, _ in request_response.content.iter_chunks():
                    await response.send(data)

                return None

        return request.app.ctx.response.bad_request


# TODO: add_route is partially unknown and as_view is partially unknown Need PR Sanic
proxy.add_route(HeliotropeImageProxyView.as_view(), "/<shuffled_image_url>")  # type: ignore
