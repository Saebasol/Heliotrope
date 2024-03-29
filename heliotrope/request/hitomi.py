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
from json import loads
from re import match
from struct import unpack
from typing import Any, Optional

from aiohttp.client import ClientSession
from sanic.log import logger
from yarl import URL

from heliotrope.domain import Galleryinfo
from heliotrope.request.base import BaseRequest


class HitomiRequest:
    def __init__(self, request: BaseRequest, index_file: list[str]):
        self.request = request
        self.index_file = index_file
        request.session.headers.update(self.headers)

    @property
    def url(self) -> URL:
        return URL("https://hitomi.la")

    @property
    def ltn_url(self) -> URL:
        return self.url.with_host("ltn.hitomi.la")

    @property
    def headers(self) -> dict[str, str]:
        return {
            "referer": self.url.human_repr(),
            "User-Agent": self.request.user_agent,
        }

    async def close(self) -> None:
        logger.debug(f"Close {self.__class__.__name__} session")
        await self.request.session.close()

    @classmethod
    async def setup(
        cls, *, index_file: list[str] = ["index-english.nozomi"], **session_options: Any
    ) -> "HitomiRequest":
        logger.debug(f"Setting up {cls.__name__}")
        request = BaseRequest(ClientSession(**session_options))
        hitomi_request = cls(request, index_file)
        return hitomi_request

    async def get_gg_js(self) -> str:
        request_url = self.ltn_url.with_path("gg.js")
        response = await self.request.get(request_url, "text")
        return str(response.body)

    async def get_redirect_url(self, id: int) -> Optional[tuple[str, str]]:
        request_url = self.url.with_path(f"galleries/{id}.html")
        response = await self.request.get(request_url, "text")
        if response.status != 200:
            return None

        matched = match(r"window\.location\.href = \"(.+?)\"", response.body)
        assert matched
        url = matched.group(1)
        hitomi_type = URL(url).path.split("/")[1]
        return url, hitomi_type

    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        request_url = self.ltn_url.with_path(f"galleries/{id}.js")
        response = await self.request.get(request_url, "text")

        if response.status != 200:
            return None

        js_to_json = loads(str(response.body).replace("var galleryinfo = ", ""))

        return Galleryinfo.from_dict(js_to_json)

    # NOTE: See https://ltn.hitomi.la/galleryblock.js
    # 참고: https://ltn.hitomi.la/galleryblock.js
    async def fetch_index(
        self,
        page: int = 1,
        item: int = 25,
        include_range: bool = True,
    ) -> list[int]:

        byte_start = (page - 1) * item * 4
        byte_end = byte_start + item * 4 - 1

        headers = {
            "origin": self.url.human_repr(),
        }
        if include_range:
            headers.update({"Range": f"bytes={byte_start}-{byte_end}"})

        index: list[int] = []
        for index_file in self.index_file:
            request_url = self.ltn_url.with_path(index_file)
            response = await self.request.get(request_url, "read", headers=headers)
            total_items = len(response.body) // 4
            index.extend(unpack(f">{total_items}i", bytes(response.body)))
        return index
