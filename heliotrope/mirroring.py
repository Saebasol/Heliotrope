import asyncio
import datetime
import time

from aiohttp.client import ClientSession

from heliotrope.database.query import get_index, put_galleryinfo, put_index
from heliotrope.utils.requester import HitomiRequester


class Mirroring(HitomiRequester):
    def __init__(self, session: ClientSession) -> None:
        super().__init__(session)
        self.last_checked_time = None
        self.mirroring_time = None
        self.new_item = None
        self.status = "idle"

    async def compare_index(self):
        remote_index_list = await self.fetch_index()
        local_index_list = await get_index()

        return list(set(remote_index_list) - set(local_index_list))

    async def start_mirroring_with_index_list(self, index_list):
        for index in index_list:
            if galleryinfo := await self.get_galleryinfo(index):
                await put_galleryinfo(galleryinfo)

            await put_index(index)
        self.mirroring_time = f"({time.tzname[0]}) {datetime.datetime.now()}"
        self.new_item = str(len(index_list))

    async def mirroring_task(self, delay: float):
        while True:
            self.last_checked_time = f"({time.tzname[0]}) {datetime.datetime.now()}"
            if index_list := await self.compare_index():
                self.status = "mirorring"
                await self.start_mirroring_with_index_list(index_list)
            self.status = "idle"

            await asyncio.sleep(delay)
