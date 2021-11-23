from dataclasses import dataclass
from typing import Any, Literal

from aiohttp.client import ClientSession
from multidict import CIMultiDictProxy
from yarl import URL


@dataclass
class Response:
    status: int
    returned: Any
    url: URL
    headers: CIMultiDictProxy[str]


class BaseRequest:
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    @property
    def user_agent(self) -> str:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any
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
        url: str,
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any
    ) -> Response:
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self,
        url: str,
        return_method: Literal["json", "text", "read"] = "json",
        **kwargs: Any
    ) -> Response:
        return await self.request("POST", url, return_method, **kwargs)
