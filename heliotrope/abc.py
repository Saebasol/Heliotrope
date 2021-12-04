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
from typing import Optional
from heliotrope.domain import Galleryinfo, Info
from heliotrope.types import HitomiGalleryinfoJSON
from typing import NoReturn


class AbstractSQL:
    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> None:
        raise NotImplementedError

    async def get_galleryinfo(
        self, galleryinfo_id: int
    ) -> Optional[HitomiGalleryinfoJSON]:
        raise NotImplementedError

    async def get_all_index(self) -> list[int]:
        raise NotImplementedError


class AbstractNoSQL:
    async def add_infos(self, infos: list[Info]) -> None:
        ...

    async def get_info(self, id: int) -> Info:
        ...

    async def get_list(self, offset: int = 0, limit: int = 15) -> list[Info]:
        ...

    async def search(
        self,
        tags: list[str],
        offset: int = 0,
        limit: int = 15,
    ) -> list[Info]:
        ...


class AbstractTask:
    async def start(self, delay: float) -> NoReturn:
        raise NotImplementedError
