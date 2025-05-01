from re import match
from typing import Optional, cast
from urllib.parse import unquote

from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage, NotFound
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.infrastructure.sanic import HeliotropeRequest

proxy_endpoint = Blueprint("proxy", url_prefix="/proxy")


class HeliotropeImageProxyView(HTTPMethodView):
    @openapi.tag("proxy")
    @openapi.summary("Proxy image")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="image_url", location="path", schema=str
    )
    async def get(
        self, request: HeliotropeRequest, image_url: str
    ) -> Optional[HTTPResponse]:
        # Unquote url first
        # url 디코딩
        unquote_image_url = unquote(image_url)

        # Check url is pixiv and hitomi
        # url이 히토미 또는 픽시브인지 확인
        if not match(
            r"https:\/\/.+?(\.gold-usergeneratedcontent\.net|\.pximg\.net)",
            unquote_image_url,
        ):
            raise InvalidUsage

        headers = request.app.ctx.hitomi_la.headers

        # Pixiv request header
        # 픽시브일경우 리퍼러 헤더 변경
        if "pximg" in unquote_image_url:
            headers.update({"referer": "https://pixiv.net"})

        async with request.app.ctx.hitomi_la.session.get(
            unquote_image_url, headers=headers
        ) as request_response:
            if request_response.status != 200:
                raise NotFound

            response = cast(
                HTTPResponse,
                await request.respond(content_type=request_response.content_type),
            )

            # Use chunk
            # 청크를 사용
            # If read is used, oom may occur if many images are requested.
            # 만약 .read를 사용할경우 메모리를 많이 먹기때문에 많은 요청 들어오면 out of memory로 터질수도있음
            async for data, _ in request_response.content.iter_chunks():
                await response.send(data)
            return await response.eof()


proxy_endpoint.add_route(
    HeliotropeImageProxyView.as_view(), "/<image_url:path>", unquote=True
)
