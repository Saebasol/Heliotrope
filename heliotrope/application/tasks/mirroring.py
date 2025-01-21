from asyncio import gather, sleep
from dataclasses import dataclass
from typing import Any, Callable, Coroutine
from heliotrope.core.galleryinfo.domain.entity import Galleryinfo
from heliotrope.core.info.domain.entity import Info
from heliotrope.core.info.usecases.add import BulkAddInfoUseCase
from heliotrope.core.info.usecases.get import GetAllInfoIdsUseCase
from heliotrope.core.serializer import Serializer
from heliotrope.infrastructure.hitomila.galleryinfo.domain.repository import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.mongodb.info.domain.repository import (
    MongoDBInfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.repository import (
    SAGalleryinfoRepository,
)
from heliotrope.core.galleryinfo.usecases.get import (
    GetAllGalleryinfoIdsUseCase,
    GetGalleryinfoUseCase,
)
from heliotrope.core.galleryinfo.usecases.add import (
    AddGalleryinfoUseCase,
)

from datetime import datetime
from time import tzname


def now():
    return f"({tzname[0]}) {datetime.now()}"


@dataclass
class MirroringProgress(Serializer):
    total: int
    job_total: int
    job_completed: int
    mirrored: int
    is_mirroring_galleryinfo: bool
    is_converting_to_info: bool
    last_checked: str
    last_mirrored: str

    def reset(self) -> None:
        self.job_completed = 0
        self.total = 0
        self.job_total = 0


class MirroringTask:
    CONCURRENT_SIZE: int = 100

    def __init__(
        self,
        hitomi_la: HitomiLaGalleryinfoRepository,
        sqlalchemy: SAGalleryinfoRepository,
        mongodb: MongoDBInfoRepository,
    ) -> None:
        self.hitomi_la = hitomi_la
        self.sqlalchemy = sqlalchemy
        self.mongodb = mongodb
        self.progress = MirroringProgress(0, 0, 0, 0, False, False, "", "")

    # Edge case: 1783616 <=> 1669497
    async def _preprocess(
        self, execute: Callable[[int], Coroutine[Any, Any, Galleryinfo]], id: int
    ) -> Galleryinfo:
        galleryinfo = await execute(id)
        galleryinfo.id = id
        return galleryinfo

    async def _get_differences(
        self,
        source_usecase: GetAllGalleryinfoIdsUseCase,
        target_usecase: GetAllGalleryinfoIdsUseCase | GetAllInfoIdsUseCase,
    ) -> list[int]:
        source_ids = await source_usecase.execute()
        target_ids = await target_usecase.execute()
        return list(set(source_ids) - set(target_ids))

    async def _process_in_jobs(
        self, ids: list[int], process_function: Callable[[list[int]], Any]
    ) -> None:
        jobs = [
            ids[i : i + self.CONCURRENT_SIZE]
            for i in range(0, len(ids), self.CONCURRENT_SIZE)
        ]
        self.progress.total = len(ids)
        self.progress.job_total = len(jobs)
        for job in jobs:
            await process_function(job)
            self.progress.job_completed += 1

        self.progress.reset()
        self.progress.mirrored = len(ids)

    async def _fetch_and_store_galleryinfo(
        self, ids: list[int], target_repository: SAGalleryinfoRepository
    ) -> None:
        tasks = [
            self._preprocess(GetGalleryinfoUseCase(self.hitomi_la).execute, id)
            for id in ids
        ]
        results = await gather(*tasks)
        for result in results:
            await AddGalleryinfoUseCase(target_repository).execute(result)

    async def _fetch_and_store_info(self, ids: list[int]) -> None:
        tasks = [GetGalleryinfoUseCase(self.sqlalchemy).execute(id) for id in ids]
        results = await gather(*tasks)
        infos = list(map(Info.from_galleryinfo, results))
        await BulkAddInfoUseCase(self.mongodb).execute(infos)

    async def mirror(self) -> None:
        remote_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.hitomi_la),
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
        )

        if remote_differences:
            self.progress.is_mirroring_galleryinfo = True
            await self._process_in_jobs(
                remote_differences,
                lambda batch: self._fetch_and_store_galleryinfo(batch, self.sqlalchemy),
            )
            self.progress.is_mirroring_galleryinfo = False

        local_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.hitomi_la),
            GetAllInfoIdsUseCase(self.mongodb),
        )

        if local_differences:
            self.progress.is_converting_to_info = True
            await self._process_in_jobs(local_differences, self._fetch_and_store_info)
            self.progress.is_converting_to_info = False

        self.progress.last_mirrored = now()

    async def start(self, delay: float) -> None:
        while True:
            self.progress.last_checked = now()
            await self.mirror()
            await sleep(delay)
