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
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.types import Schema

from heliotrope.sanic import HeliotropeRequest

hitomi_random = Blueprint("hitomi_random", url_prefix="/random")


class HitomiRandomView(HTTPMethodView):
    @openapi.summary("Get random result in hitomi")  # type: ignore
    @openapi.tag("hitomi")  # type: ignore
    @openapi.body(  # type: ignore
        {
            "application/json": openapi.Object(
                {
                    "query": Schema.make(value=["language:korean"]),  # type: ignore
                }
            )
        }
    )
    async def post(self, request: HeliotropeRequest) -> HTTPResponse:
        query: list[str] = request.json.get("query") if request.json else []
        info = await request.app.ctx.odm.get_random_info(query)

        return json(
            {"status": 200, **await request.app.ctx.common_js.convert_thumbnail(info)}
        )


hitomi_random.add_route(HitomiRandomView.as_view(), "/")
