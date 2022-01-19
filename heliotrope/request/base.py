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
from dataclasses import dataclass
from typing import Any, Literal, Union

from aiohttp.client import ClientSession
from multidict import CIMultiDictProxy
from sanic.log import logger
from yarl import URL


@dataclass
class Response:
    status: int
    body: Any
    url: URL
    headers: CIMultiDictProxy[str]


class BaseRequest:
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    @property
    def user_agent(self) -> str:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

    @classmethod
    async def setup(cls) -> "BaseRequest":
        logger.debug(f"Setting up {cls.__name__}")
        return cls(ClientSession())

    async def close(self) -> None:
        logger.debug(f"Close {self.__class__.__name__} session")
        await self.session.close()

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: Union[str, URL],
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any,
    ) -> Response:

        async with self.session.request(method, url, **kwargs) as r:
            return Response(
                r.status,
                await getattr(r, return_method)(),
                r.url,
                r.headers,
            )

    async def get(
        self,
        url: Union[str, URL],
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any,
    ) -> Response:
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self,
        url: Union[str, URL],
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any,
    ) -> Response:
        return await self.request("POST", url, return_method, **kwargs)
