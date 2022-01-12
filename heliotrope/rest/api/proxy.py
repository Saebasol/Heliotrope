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
from typing import Optional
from urllib.parse import unquote

from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage, NotFound
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi  # type: ignore

from heliotrope.sanic import HeliotropeRequest

heliotrope_image_proxy = Blueprint("proxy", url_prefix="/proxy")


class HeliotropeImageProxyView(HTTPMethodView):
    @openapi.tag("proxy")  # type: ignore
    @openapi.summary("Proxy image")  # type: ignore
    @openapi.parameter(name="image_url", location="path", schema=str)  # type: ignore
    async def get(
        self, request: HeliotropeRequest, image_url: str
    ) -> Optional[HTTPResponse]:
        # Unquote url first
        # url 디코딩
        unquote_image_url = unquote(image_url)

        # Check url is pixiv and hitomi
        # url이 히토미 또는 픽시브인지 확인
        if not match(r"https:\/\/.+?(\.hitomi\.la|\.pximg\.net)", unquote_image_url):
            raise InvalidUsage

        headers = request.app.ctx.hitomi_request.headers

        # Pixiv request header
        # 픽시브일경우 리퍼러 헤더 변경
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
            # 청크를 사용
            # If read is used, oof may occur if many images are requested.
            # 만약 .read를 사용할경우 메모리를 많이 먹기때문에 많은 요청 들어오면 out of memory로 터질수도있음
            async for data, _ in request_response.content.iter_chunks():
                await response.send(data)
            return await response.eof()  # type: ignore


heliotrope_image_proxy.add_route(
    HeliotropeImageProxyView.as_view(), "/<image_url:path>", unquote=True
)
