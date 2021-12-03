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
from struct import unpack
from typing import Any, Optional

from aiohttp.client import ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag
from yarl import URL

from heliotrope.domain import Galleryinfo
from heliotrope.request.base import BaseRequest
from heliotrope.types import HitomiGalleryinfoJSON


class HitomiRequest(BaseRequest):
    def __init__(self, session: ClientSession, index_file: str):
        super().__init__(session)
        self.index_file = index_file

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
            "User-Agent": self.user_agent,
        }

    @classmethod
    async def setup(
        cls, *, index_file: str = "index-korean.nozomi", **session_options: Any
    ) -> "HitomiRequest":
        session = ClientSession(**session_options)
        hitomi_request_instance = cls(session, index_file)
        hitomi_request_instance.session.headers.update(hitomi_request_instance.headers)
        return hitomi_request_instance

    async def get_common_js(self) -> str:
        request_url = self.ltn_url.with_path("common.js").human_repr()
        response = await self.get(request_url, "text")
        return str(response.returned)

    async def get_redirect_url(self, index_id: int) -> Optional[tuple[str, str]]:
        request_url = self.url.with_path(f"galleries/{index_id}.html").human_repr()
        response = await self.get(request_url, "text")
        if response.status != 200:
            return None

        soup = BeautifulSoup(response.returned, "lxml")
        a_href_element = soup.find("a", href=True)
        assert isinstance(a_href_element, Tag)
        url = a_href_element.attrs["href"]
        hitomi_type = URL(url).path.split("/")[1]
        return url, hitomi_type

    async def get_galleryinfo(self, index_id: int) -> Optional[Galleryinfo]:
        request_url = self.ltn_url.with_path(f"galleries/{index_id}.js").human_repr()
        response = await self.get(request_url, "text")

        if response.status != 200:
            return None

        js_to_json = loads(str(response.returned).replace("var galleryinfo = ", ""))

        return Galleryinfo.from_dict(js_to_json)

    async def fetch_index(
        self,
        page: int = 1,
        item: int = 25,
        include_range: bool = True,
    ) -> tuple[int, ...]:
        byte_start = (page - 1) * item * 4
        byte_end = byte_start + item * 4 - 1

        headers = {
            "origin": self.url.human_repr(),
        }
        if include_range:
            headers.update({"Range": f"bytes={byte_start}-{byte_end}"})

        request_url = self.ltn_url.with_path(self.index_file).human_repr()
        response = await self.get(request_url, "read", headers=headers)

        total_items = len(response.returned) // 4
        return unpack(f">{total_items}i", bytes(response.returned))
