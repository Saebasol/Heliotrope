from sanic import Blueprint
from sanic.views import HTTPMethodView

from heliotrope.utils.response import bad_request
from heliotrope.utils.shuffle import solve_shuffle_image_url
from heliotrope.utils.typed import HeliotropeRequest

heliotrope_image_proxy = Blueprint("heliotrope_image_proxy", url_prefix="/proxy")


class HeliotropeImageProxyView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, shuffled_url: str):
        url = solve_shuffle_image_url(shuffled_url)
        if not url:
            return bad_request

        headers = {
            "referer": f"https://{request.app.ctx.hitomi_requester.domain}",
            "User-Agent": request.app.ctx.hitomi_requester.user_agent,
        }
        if "pximg" in url:
            headers.update({"referer": "https://pixiv.net"})

        async with request.app.ctx.hitomi_requester.session.get(
            url, headers=headers
        ) as r:
            if r.status != 200:
                return bad_request

            response = await request.respond(content_type=r.content_type)
            async for data, _ in r.content.iter_chunks():
                await response.send(data)


heliotrope_image_proxy.add_route(HeliotropeImageProxyView.as_view(), "/<shuffled_url>")
