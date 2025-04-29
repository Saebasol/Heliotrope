from typing import Generator

from aiohttp import ClientSession
from yarl import URL


class HitomiLa:
    def __init__(self, session: ClientSession, index_files: list[str]) -> None:
        self.session = session
        self.index_files = index_files

    @property
    def base_url(self) -> URL:
        return URL("https://hitomi.la")

    @property
    def ltn_url(self) -> URL:
        return URL("https://ltn.gold-usergeneratedcontent.net/")

    @property
    def index_url(self) -> Generator[URL, None, None]:
        for index_file in self.index_files:
            yield self.ltn_url.with_path(index_file)

    @property
    def user_agent(self) -> str:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    @property
    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "origin": self.base_url.human_repr(),
            "referer": self.base_url.human_repr(),
        }

    @classmethod
    async def create(cls, index_files: list[str]) -> "HitomiLa":
        return cls(ClientSession(), index_files)
