import json
from dataclasses import dataclass
from struct import unpack
from typing import Any, Literal
from urllib.parse import urlparse

from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL
from bs4 import BeautifulSoup
from multidict import CIMultiDictProxy
from yarl import URL

from heliotrope.utils.decorators import strict_literal
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel, HitomiTagsModel


@dataclass
class Response:
    status: int
    reason: str
    body: Any
    url: URL
    headers: CIMultiDictProxy[str]


class SessionRequester:
    def __init__(self, session: ClientSession = None) -> None:
        self.session = session

    @strict_literal("return_method")
    async def request(
        self,
        method: str,
        url: StrOrURL,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any,
    ):
        if not self.session:
            raise RuntimeError("Need ClientSession")
        async with self.session.request(method, url, **kwargs) as r:
            return Response(
                r.status,
                r.reason,
                await getattr(r, return_method)(),
                r.url,
                r.headers,
            )

    @strict_literal("return_method")
    async def get(
        self,
        url: StrOrURL,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any,
    ):
        return await self.request("GET", url, return_method, **kwargs)

    @strict_literal("return_method")
    async def post(
        self,
        url: StrOrURL,
        return_method: Literal["read", "text", "json"],
        **kwargs: Any,
    ):
        return await self.request("POST", url, return_method, **kwargs)


# class SemaphoreRequester:
#     def __init__(self, semaphore: Semaphore = None) -> None:
#         self.semaphore = semaphore

#     @strict_literal("return_method")
#     async def request(
#         self,
#         method: str,
#         url: StrOrURL,
#         return_method: Literal["read", "text", "json"],
#         **kwargs: Any,
#     ):
#         if not self.semaphore:
#             raise RuntimeError("Need Semaphore")
#         async with ClientSession() as cs:
#             async with self.semaphore, cs.request(method, url, **kwargs) as r:
#                 return Response(
#                     r.status,
#                     r.reason,
#                     await getattr(r, return_method)(),
#                     r.url,
#                     r.headers,
#                 )

#     @strict_literal("return_method")
#     async def get(
#         self,
#         url: StrOrURL,
#         return_method: Literal["read", "text", "json"],
#         **kwargs: Any,
#     ):
#         return await self.request("GET", url, return_method, **kwargs)

#     @strict_literal("return_method")
#     async def post(
#         self,
#         url: StrOrURL,
#         return_method: Literal["read", "text", "json"],
#         **kwargs: Any,
#     ):
#         return await self.request("POST", url, return_method, **kwargs)


class HitomiRequester(SessionRequester):
    domain = "hitomi.la"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    headers = {"referer": f"https://{domain}", "User-Agent": user_agent}

    def __init__(self, session: ClientSession) -> None:
        super().__init__(session=session)

    async def get_redirect_url(self, index: int):
        response = await self.get(
            f"https://{self.domain}/galleries/{index}.html",
            "text",
            headers=self.headers,
        )
        if response.status != 200:
            return
        soup = BeautifulSoup(response.body, "lxml")
        url = soup.find("a", href=True)["href"]
        hitomi_type = urlparse(url).path.split("/")[1]
        # index = re.search(r"\-([0-9]*)\.html", "url")[1]
        return url, hitomi_type

    async def get_galleryinfo(self, index: int, parse: bool = False):
        response = await self.get(
            f"https://ltn.{self.domain}/galleries/{index}.js",
            "text",
            headers=self.headers,
        )
        if response.status != 200:
            return
        js_to_json = str(response.body).replace("var galleryinfo = ", "")
        return HitomiGalleryInfoModel.parse_galleryinfo(json.loads(js_to_json), parse)

    async def fetch_index(
        self, page: int = 1, item: int = 25, index_file: str = "index-korean.nozomi"
    ):
        byte_start = (page - 1) * item * 4
        byte_end = byte_start + item * 4 - 1

        response = await self.get(
            f"https://ltn.{self.domain}/{index_file}",
            "read",
            headers={
                "User-Agent": self.user_agent,
                "Range": f"byte={byte_start}-{byte_end}",
                "referer": f"https://{self.domain}/index-all-{page}.html",
                "origin": f"http://{self.domain}",
            },
        )

        # Check 32bit
        # len(buffer) % 4

        total_items = len(response.body) // 4
        return unpack(f">{total_items}i", bytes(response.body))

    async def get_info_using_index(self, index: int):
        if url_hitomi_type_tuple := await self.get_redirect_url(index):
            url, hitomi_type = url_hitomi_type_tuple
            response = await self.get(url, "text")

            if tags_model := HitomiTagsModel.parse_tags(response.body, hitomi_type):
                return {
                    "title": tags_model.title,
                    "thumbnail": tags_model.thumbnail,
                    "artist": tags_model.artist,
                    "group": tags_model.group,
                    "type": tags_model.hitomi_type,
                    "language": tags_model.language,
                    "series": tags_model.series,
                    "characters": tags_model.characters,
                    "tags": tags_model.tags,
                }
