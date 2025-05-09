from asyncio import as_completed, sleep
from dataclasses import dataclass
from datetime import datetime
from time import tzname
from typing import Any, Callable, Coroutine

import memray
from sanic.log import logger

from heliotrope.application.usecases.create.galleryinfo import CreateGalleryinfoUseCase
from heliotrope.application.usecases.create.info import CreateInfoUseCase
from heliotrope.application.usecases.get.galleryinfo import (
    GetAllGalleryinfoIdsUseCase,
    GetGalleryinfoUseCase,
)
from heliotrope.application.usecases.get.info import GetAllInfoIdsUseCase
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.info import Info
from heliotrope.domain.serializer import Serializer
from heliotrope.infrastructure.hitomila.repositories.galleryinfo import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.mongodb.repositories.info import MongoDBInfoRepository
from heliotrope.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)


def now() -> str:
    return f"({tzname[0]}) {datetime.now()}"


class Proxy:
    def __init__(self, progress_dict: dict[str, Any]) -> None:
        self.progress_dict = progress_dict

    def reset(self) -> None:
        self.job_completed = 0
        self.total = 0
        self.job_total = 0

    def __getattr__(self, name: str) -> Any:
        if name in self.progress_dict:
            return self.progress_dict[name]

        return super().__getattr__(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAttributeAccessIssue]
            name
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "progress_dict":
            super().__setattr__(name, value)
        else:
            self.progress_dict[name] = value


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

    @classmethod
    def default(cls) -> "MirroringProgress":
        return cls(
            total=0,
            job_total=0,
            job_completed=0,
            mirrored=0,
            is_mirroring_galleryinfo=False,
            is_converting_to_info=False,
            last_checked="",
            last_mirrored="",
        )


class MirroringTask:
    CONCURRENT_SIZE: int = 100

    def __init__(
        self,
        hitomi_la: HitomiLaGalleryinfoRepository,
        sqlalchemy: SAGalleryinfoRepository,
        mongodb: MongoDBInfoRepository,
        mirroring_progress_dict: dict[str, Any],
    ) -> None:
        self.hitomi_la = hitomi_la
        self.sqlalchemy = sqlalchemy
        self.mongodb = mongodb
        self.progress = Proxy(mirroring_progress_dict)

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
        for result in as_completed(tasks):
            result = await result
            await CreateGalleryinfoUseCase(target_repository).execute(result)

    async def _fetch_and_store_info(self, ids: list[int]) -> None:
        tasks = [GetGalleryinfoUseCase(self.sqlalchemy).execute(id) for id in ids]
        for result in as_completed(tasks):
            result = await result
            await CreateInfoUseCase(self.mongodb).execute(Info.from_galleryinfo(result))

    async def mirror(self) -> None:
        mirroring_is_end = False
        remote_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.hitomi_la),
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
        )

        if remote_differences:
            mirroring_is_end = True
            self.progress.is_mirroring_galleryinfo = True
            await self._process_in_jobs(
                remote_differences,
                lambda batch: self._fetch_and_store_galleryinfo(batch, self.sqlalchemy),
            )
            self.progress.is_mirroring_galleryinfo = False

        local_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
            GetAllInfoIdsUseCase(self.mongodb),
        )

        if local_differences:
            self.progress.is_converting_to_info = True
            await self._process_in_jobs(local_differences, self._fetch_and_store_info)
            self.progress.is_converting_to_info = False

        if mirroring_is_end:
            self.progress.last_mirrored = now()

    async def start(self, delay: float) -> None:
        logger.info(f"Starting Mirroring task with delay: {delay}")
        while True:
            self.progress.last_checked = now()
            await self.mirror()
            await sleep(delay)
