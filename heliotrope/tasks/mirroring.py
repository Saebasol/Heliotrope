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
from asyncio.tasks import sleep
from typing import NoReturn

from heliotrope.abc import AbstractSQL, AbstractTask, AbstractNoSQL
from heliotrope.request.hitomi import HitomiRequest


class MirroringTask(AbstractTask):
    def __init__(
        self, request: HitomiRequest, sql: AbstractSQL, nosql: AbstractNoSQL
    ) -> None:
        self.request = request
        self.sql = sql
        self.nosql = nosql

    async def compare_index_list(self) -> list[int]:
        remote_index_list = await self.request.fetch_index(include_range=False)
        local_index_list = await self.sql.get_all_index()
        return list(set(remote_index_list) - set(local_index_list))

    async def mirroring(self, index_list: list[int]) -> None:
        for index in index_list:
            if galleryinfo := await self.request.get_galleryinfo(index):
                if not await self.sql.get_galleryinfo(index):
                    await self.sql.add_galleryinfo(galleryinfo)

            if info := await self.request.get_info(index):
                if not await self.nosql.get_info(index):
                    await self.nosql.add_infos([info])

    async def start(self, delay: float) -> NoReturn:
        while True:
            if index_list := await self.compare_index_list():
                await self.mirroring(index_list)
                self.total = len(await self.sql.get_all_index())
            await sleep(delay)
