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
from asyncio.tasks import Task, create_task, sleep
from typing import NoReturn

from heliotrope.abc.database import AbstractGalleryinfoDatabase, AbstractInfoDatabase
from heliotrope.abc.task import AbstractTask
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.sanic import Heliotrope


class MirroringTask(AbstractTask):
    config_name = "MIRRORING_DELAY"

    def __init__(
        self,
        request: HitomiRequest,
        galleryinfo_database: AbstractGalleryinfoDatabase,
        info_database: AbstractInfoDatabase,
    ) -> None:
        self.request = request
        self.galleryinfo_database = galleryinfo_database
        self.info_database = info_database

    @classmethod
    async def setup(cls, app: Heliotrope, delay: float) -> Task[NoReturn]:
        instance = cls(app.ctx.hitomi_request, app.ctx.orm, app.ctx.meilisearch)
        return create_task(instance.start(delay))

    async def compare_index_list(self) -> list[int]:
        remote_index_list = await self.request.fetch_index(include_range=False)
        local_index_list = await self.galleryinfo_database.get_all_index()
        return list(set(remote_index_list) - set(local_index_list))

    async def mirroring(self, index_list: list[int]) -> None:
        for index in index_list:
            # Check galleryinfo first
            if galleryinfo := await self.request.get_galleryinfo(index):
                if not await self.galleryinfo_database.get_galleryinfo(index):
                    await self.galleryinfo_database.add_galleryinfo(galleryinfo)

            # Then check info
            if info := await self.request.get_info(index):
                if not await self.info_database.get_info(index):
                    await self.info_database.add_infos([info])

    async def start(self, delay: float) -> NoReturn:
        while True:
            if index_list := await self.compare_index_list():
                await self.mirroring(index_list)
                self.total = len(await self.galleryinfo_database.get_all_index())
            await sleep(delay)
