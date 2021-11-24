from typing import Any, NoReturn
from heliotrope.database.orm import ORM
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.tasks.base import AbstractTask
from asyncio.tasks import sleep


class MirroringTask(AbstractTask):
    def __init__(self, request: HitomiRequest, orm: ORM, odm: Any) -> None:
        self.request = request
        self.orm = orm
        self.odm = odm

    async def compare_index_list(self) -> list[int]:
        remote_index_list = await self.request.fetch_index(include_range=False)
        local_index_list = await self.orm.get_all_index()
        return list(set(remote_index_list) - set(local_index_list))

    async def mirroring(self, index_list: list[int]) -> None:
        for index in index_list:
            if galleryinfo := await self.request.get_galleryinfo(index):
                if not await self.orm.get_galleryinfo(index):
                    await self.orm.add_galleryinfo(galleryinfo)

            # TODO: Info

    async def start(self, delay: float) -> NoReturn:
        while True:
            if index_list := await self.compare_index_list():
                await self.mirroring(index_list)
                self.total = len(await self.orm.get_all_index())
            await sleep(delay)
