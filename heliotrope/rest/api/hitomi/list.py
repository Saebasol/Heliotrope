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
from sanic.blueprints import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.sanic import HeliotropeRequest

hitomi_list = Blueprint("hitomi_list", url_prefix="/list")


class HitomiListView(HTTPMethodView):
    @openapi.tag("hitomi")  # type: ignore
    @openapi.summary("Get latest hitomi info list")  # type: ignore
    @openapi.parameter(name="index", location="path", schema=int)
    @openapi.parameter(name="language", location="query", schema=str)
    async def get(self, request: HeliotropeRequest, index: int) -> HTTPResponse:
        total = len(await request.app.ctx.orm.get_all_index())
        language = request.args.get("language")

        start_at_zero = index - 1

        if start_at_zero < 0 or total < start_at_zero:
            raise InvalidUsage

        info_list = await request.app.ctx.odm.get_info_list(language, start_at_zero, 15)

        return json(
            {
                "status": 200,
                "list": [
                    await request.app.ctx.common_js.convert_thumbnail(info)
                    for info in info_list
                ],
                "total": total,
            }
        )


hitomi_list.add_route(HitomiListView.as_view(), "/<index:int>")
