from asyncio import as_completed, sleep
from dataclasses import dataclass
from datetime import datetime
from time import tzname
from types import CoroutineType
from typing import Any, Callable, Coroutine, Generator, cast

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
        self.progress = cast(MirroringProgress, Proxy(mirroring_progress_dict))

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
    ) -> tuple[int, ...]:
        source_ids = await source_usecase.execute()
        target_ids = await target_usecase.execute()
        return tuple(set(source_ids) - set(target_ids))

    def _id_generator(self, ids: tuple[int, ...]) -> Generator[tuple[int, ...]]:
        for i in range(0, len(ids), self.CONCURRENT_SIZE):
            yield ids[i : i + self.CONCURRENT_SIZE]

    async def _fetch_remote_galleryinfo(self, id: int) -> Galleryinfo:
        return await self._preprocess(GetGalleryinfoUseCase(self.hitomi_la).execute, id)

    async def _fetch_local_galleryinfo(self, id: int) -> Galleryinfo:
        return await GetGalleryinfoUseCase(self.sqlalchemy).execute(id)

    def _fetch_remote_galleryinfo_generator(
        self,
        ids: tuple[int, ...],
    ):
        for id in self._id_generator(ids):
            yield [self._fetch_remote_galleryinfo(id) for id in id]

    def _fetch_local_galleryinfo_generator(
        self,
        ids: tuple[int, ...],
    ):
        for id in self._id_generator(ids):
            yield [self._fetch_local_galleryinfo(id) for id in id]

    async def _run_tasks(
        self,
        tasks: list[CoroutineType[Any, Any, Galleryinfo]],
        execute: Callable[[Galleryinfo], Coroutine[Any, Any, None]],
    ):
        for task in as_completed(tasks):
            result = await task
            await execute(result)
            self.progress.mirrored += 1

        self.progress.job_completed += 1

    async def mirror(self) -> None:
        mirroring_is_end = False
        remote_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.hitomi_la),
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
        )

        if remote_differences:
            mirroring_is_end = True
            self.progress.is_mirroring_galleryinfo = True
            self.progress.total = len(remote_differences)
            self.progress.job_total = len(remote_differences) // self.CONCURRENT_SIZE

            for tasks in self._fetch_remote_galleryinfo_generator(remote_differences):
                await self._run_tasks(
                    tasks,
                    CreateGalleryinfoUseCase(self.sqlalchemy).execute,
                )

            self.progress.is_mirroring_galleryinfo = False

        local_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
            GetAllInfoIdsUseCase(self.mongodb),
        )

        if local_differences:
            self.progress.is_converting_to_info = True
            self.progress.total = len(local_differences)
            self.progress.job_total = len(local_differences) // self.CONCURRENT_SIZE

            for tasks in self._fetch_local_galleryinfo_generator(local_differences):
                await self._run_tasks(
                    tasks,
                    lambda g: CreateInfoUseCase(self.mongodb).execute(
                        Info.from_galleryinfo(g)
                    ),
                )
            self.progress.is_converting_to_info = False

        if mirroring_is_end:
            self.progress.last_mirrored = now()

    async def start(self, delay: float) -> None:
        logger.info(f"Starting Mirroring task with delay: {delay}")
        while True:
            self.progress.last_checked = now()
            await self.mirror()
            await sleep(delay)
