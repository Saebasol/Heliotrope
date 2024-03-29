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
from asyncio import create_task
from asyncio.tasks import sleep
from typing import NoReturn

from sanic.log import logger

from heliotrope.abc.database import AbstractGalleryinfoDatabase, AbstractInfoDatabase
from heliotrope.abc.task import AbstractTask
from heliotrope.domain.info import Info
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.sanic import Heliotrope
from heliotrope.types import SetupTask


class MirroringTask(AbstractTask):
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
    def setup(cls, app: Heliotrope, delay: float) -> SetupTask:
        logger.debug(f"Setting up {cls.__name__}.")
        instance = cls(app.ctx.hitomi_request, app.ctx.orm, app.ctx.odm)
        return create_task(instance.start(delay))

    async def compare_index_list(self) -> list[int]:
        remote_index_list = await self.request.fetch_index(include_range=False)
        local_galleryinfo_index_list = await self.galleryinfo_database.get_all_index()
        local_info_index_list = await self.info_database.get_all_index()
        galleryinfo_index = set(remote_index_list) - set(local_galleryinfo_index_list)
        info_index = set(remote_index_list) - set(local_info_index_list)
        return list(galleryinfo_index | info_index)

    async def mirroring(self, index_list: list[int]) -> None:
        for index in index_list:
            has_galleryinfo = False
            has_info = False
            logger.debug(f"id: {index}")
            if await self.galleryinfo_database.get_galleryinfo(index):
                has_galleryinfo = True

            if await self.info_database.get_info(index):
                has_info = True

            if galleryinfo := await self.request.get_galleryinfo(index):
                if has_galleryinfo:
                    logger.debug(f"{index} already has galleryinfo locally.")
                else:
                    logger.debug(f"{index} couldn't find that info locally.")
                    await self.galleryinfo_database.add_galleryinfo(galleryinfo)
                    logger.debug(f"Added galleryinfo {index}.")

                if has_info:
                    logger.debug(f"{index} already has info locally.")
                else:
                    logger.debug(f"{index} couldn't find that galleryinfo locally.")
                    await self.info_database.add_info(
                        Info.from_galleryinfo(galleryinfo)
                    )
                    logger.debug(f"Added info {index}.")
            else:
                logger.warning(f"{index} can't get galleryinfo from hitomi.la.")

    async def start(self, delay: float) -> NoReturn:
        while True:
            if index_list := await self.compare_index_list():
                logger.warning(f"{len(index_list)} new index found.")
                logger.info(f"Start mirroring.")
                await self.mirroring(index_list)
                logger.info(f"Mirroring finished.")
            await sleep(delay)
