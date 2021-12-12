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

from heliotrope.sanic import HeliotropeRequest

hitomi_search = Blueprint("hitomi_search", url_prefix="/search")


class HitomiSearchView(HTTPMethodView):
    async def post(self, request: HeliotropeRequest) -> HTTPResponse:
        offset = (
            int(offset) - 1
            if (offset := request.json.get("offset")) and not (int(offset) - 1 < 0)
            else 0
        )
        if (query := request.json.get("query")) and query:
            results, count = await request.app.ctx.meilisearch.search(query, offset)
            return json(
                {
                    "status": 200,
                    "result": [result.to_dict() for result in results],
                    "count": count,
                }
            )
        raise InvalidUsage


hitomi_search.add_route(HitomiSearchView.as_view(), "/")
