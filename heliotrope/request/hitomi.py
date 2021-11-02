from json import loads
from struct import unpack
from typing import Any, Mapping, Optional, cast
from urllib.parse import urlparse

from aiohttp.client import ClientSession
from bs4 import BeautifulSoup  # type: ignore

from heliotrope.hitomi.models import HitomiGalleryinfo, HitomiInfo
from heliotrope.request.base import BaseRequest
from heliotrope.typing import HitomiGalleryinfoJSON


class HitomiRequest(BaseRequest):
    def __init__(self, session: ClientSession, index_file: str = "index-korean.nozomi"):
        super().__init__(session)
        self.index_file = index_file

    @property
    def domain(self) -> str:
        return "hitomi.la"

    @property
    def headers(self) -> dict[str, str]:
        return {
            "referer": f"https://{self.domain}",
            "User-Agent": self.user_agent,
        }

    @property
    def ltn_url(self) -> str:
        return f"https://ltn.{self.domain}"

    @property
    def url(self) -> str:
        return f"https://{self.domain}"

    @classmethod
    async def setup(cls, **kwargs: Any) -> "HitomiRequest":
        index_file = kwargs.pop("index_file", "index-korean.nozomi")
        session = ClientSession(**kwargs)
        hitomi_request = cls(session, index_file)
        hitomi_request.session.headers.update(hitomi_request.headers)
        return hitomi_request

    async def get_common_js(self) -> str:
        response = await self.get(f"{self.ltn_url}/common.js", "text")
        return cast(str, response.returned)

    async def get_redirect_url(self, index_id: int) -> Optional[tuple[str, str]]:
        response = await self.get(f"{self.url}/galleries/{index_id}.html", "text")
        if response.status != 200:
            return None

        soup = BeautifulSoup(response.returned, "lxml")
        url = cast(Mapping[str, str], soup.find("a", href=True))["href"]
        hitomi_type = urlparse(url).path.split("/")[1]
        return url, hitomi_type

    async def get_galleryinfo(self, index_id: int) -> Optional[HitomiGalleryinfo]:
        response = await self.get(f"{self.ltn_url}/galleries/{index_id}.js", "text")

        if response.status != 200:
            return None

        js_to_json = cast(
            HitomiGalleryinfoJSON,
            loads(str(response.returned).replace("var galleryinfo = ", "")),
        )
        return HitomiGalleryinfo(js_to_json)

    async def fetch_index(
        self,
        page: int = 1,
        item: int = 25,
        include_range: bool = True,
    ) -> tuple[int, ...]:
        byte_start = (page - 1) * item * 4
        byte_end = byte_start + item * 4 - 1

        headers = {
            "origin": f"http://{self.domain}",
        }
        if include_range:
            headers.update({"Range": f"bytes={byte_start}-{byte_end}"})

        response = await self.get(
            f"{self.ltn_url}/{self.index_file}", "read", headers=headers
        )

        total_items = len(response.returned) // 4
        return unpack(f">{total_items}i", bytes(response.returned))

    async def get_info(self, index_id: int) -> Optional[HitomiInfo]:
        if url_hitomi_type_tuple := await self.get_redirect_url(index_id):
            url, hitomi_type = url_hitomi_type_tuple
            response = await self.get(url, "text")

            # Some pages are not founds
            if response.status != 200 or "Redirect" in response.returned:
                return None

            if isinstance(response.returned, bytes):
                response.returned = response.returned.decode("utf-8")

            return HitomiInfo(response.returned, hitomi_type)

        return None
