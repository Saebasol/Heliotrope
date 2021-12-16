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
from sanic.exceptions import NotFound
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi  # type: ignore

from heliotrope.sanic import HeliotropeRequest

hitomi_galleryinfo = Blueprint("hitomi_galleryinfo", url_prefix="/galleryinfo")


class HitomiGalleryinfoView(HTTPMethodView):
    @openapi.tag("hitomi")  # type: ignore
    @openapi.summary("Get hitomi galleryinfo")  # type: ignore
    @openapi.parameter(name="id", location="path", schema=int)  # type: ignore
    async def get(self, request: HeliotropeRequest, id: int) -> HTTPResponse:
        if galleryinfo := await request.app.ctx.orm.get_galleryinfo(id):
            return json({"status": 200, **galleryinfo.to_dict()})

        if requested_galleryinfo := await request.app.ctx.hitomi_request.get_galleryinfo(
            id
        ):
            return json({"status": 200, **requested_galleryinfo.to_dict()})

        raise NotFound


hitomi_galleryinfo.add_route(HitomiGalleryinfoView.as_view(), "/<id:int>")
