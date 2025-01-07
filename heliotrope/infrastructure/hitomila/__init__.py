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
        return self.base_url.with_host("ltn.hitomi.la")

    @property
    def index_url(self) -> Generator[URL, None, None]:
        for index_file in self.index_files:
            yield self.ltn_url.with_path(index_file)

    @classmethod
    async def create(cls, index_files: list[str]) -> "HitomiLa":
        return cls(ClientSession(), index_files)
