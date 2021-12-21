"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from re import match
from urllib.parse import unquote

from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage, NotFound
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi  # type: ignore

from heliotrope.sanic import HeliotropeRequest

heliotrope_image_proxy = Blueprint("proxy", url_prefix="/proxy")


class HeliotropeImageProxyView(HTTPMethodView):
    @openapi.tag("hitomi")  # type: ignore
    @openapi.summary("Proxy image")  # type: ignore
    @openapi.parameter(name="image_url", location="path", schema=str)  # type: ignore
    async def get(self, request: HeliotropeRequest, image_url: str) -> HTTPResponse:
        # Unquote url first
        unquote_image_url = unquote(image_url)

        # Check url is pixiv and hitomi
        if not match(r"https:\/\/.+?(\.hitomi\.la|\.pximg\.net)", unquote_image_url):
            raise InvalidUsage

        headers = request.app.ctx.hitomi_request.headers

        # Pixiv request header
        if "pximg" in unquote_image_url:
            headers.update({"referer": "https://pixiv.net"})

        async with request.app.ctx.request.session.get(
            unquote_image_url, headers=headers
        ) as request_response:

            if request_response.status != 200:
                raise NotFound

            response: HTTPResponse = await request.respond(
                content_type=request_response.content_type
            )

            # Use chunk
            # If read is used, oof may occur if many images are requested.
            async for data, _ in request_response.content.iter_chunks():
                await response.send(data)
            await response.eof()  # type: ignore
            return response


heliotrope_image_proxy.add_route(HeliotropeImageProxyView.as_view(), "/<image_url:str>")
