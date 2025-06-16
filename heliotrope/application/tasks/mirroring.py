from asyncio import Lock, as_completed, sleep
from dataclasses import dataclass
from datetime import datetime
from time import tzname
from typing import Any, Callable, Coroutine, Generator, cast

from deepdiff import DeepDiff
from sanic.log import logger

from heliotrope.application.usecases.create.galleryinfo import CreateGalleryinfoUseCase
from heliotrope.application.usecases.create.info import CreateInfoUseCase
from heliotrope.application.usecases.delete.galleryinfo import DeleteGalleryinfoUseCase
from heliotrope.application.usecases.delete.info import DeleteInfoUseCase
from heliotrope.application.usecases.get.galleryinfo import (
    GetAllGalleryinfoIdsUseCase,
    GetGalleryinfoUseCase,
)
from heliotrope.application.usecases.get.info import GetAllInfoIdsUseCase
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.info import Info
from heliotrope.domain.exceptions import GalleryinfoNotFound
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
    index_files: list[str]
    total: int
    job_total: int
    job_completed: int
    mirrored: int
    is_mirroring_galleryinfo: bool
    is_converting_to_info: bool
    is_integrity_checking: bool
    last_checked: str
    last_mirrored: str

    def reset(self) -> None:
        self.job_completed = 0
        self.total = 0
        self.job_total = 0

    @classmethod
    def default(cls) -> "MirroringProgress":
        return cls(
            index_files=[],
            total=0,
            job_total=0,
            job_completed=0,
            mirrored=0,
            is_mirroring_galleryinfo=False,
            is_converting_to_info=False,
            is_integrity_checking=False,
            last_checked="",
            last_mirrored="",
        )


class MirroringTask:
    REMOTE_CONCURRENT_SIZE: int = 50
    LOCAL_CONCURRENT_SIZE: int = 25

    def __init__(
        self,
        hitomi_la_repo: HitomiLaGalleryinfoRepository,
        sqlalchemy_repo: SAGalleryinfoRepository,
        mongodb_repo: MongoDBInfoRepository,
        mirroring_progress_dict: dict[str, Any],
    ) -> None:
        self.hitomi_la = hitomi_la_repo
        self.sqlalchemy = sqlalchemy_repo
        self.mongodb = mongodb_repo
        self.progress = cast(MirroringProgress, Proxy(mirroring_progress_dict))
        self.progress.index_files = hitomi_la_repo.hitomi_la.index_files
        self._task_lock = Lock()

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

    def _get_splited_id(
        self, ids: tuple[int, ...], size: int
    ) -> Generator[tuple[int, ...]]:
        for i in range(0, len(ids), size):
            yield tuple(ids[i : i + size])

    async def _process_in_jobs(
        self,
        ids: tuple[int, ...],
        process_function: Callable[[tuple[int, ...]], Any],
        *,
        is_remote: bool,
    ) -> None:
        size = self.REMOTE_CONCURRENT_SIZE if is_remote else self.LOCAL_CONCURRENT_SIZE
        self.progress.total = len(ids)
        self.progress.job_total = len(ids) // size

        for job in self._get_splited_id(ids, size):
            await process_function(job)
            self.progress.job_completed += 1

        self.progress.reset()
        self.progress.mirrored = len(ids)

    async def _fetch_and_store_galleryinfo(
        self, ids: tuple[int, ...], target_repository: SAGalleryinfoRepository
    ) -> None:
        tasks = [
            self._preprocess(GetGalleryinfoUseCase(self.hitomi_la).execute, id)
            for id in ids
        ]
        for result in as_completed(tasks):
            result = await result
            await CreateGalleryinfoUseCase(target_repository).execute(result)

    async def _fetch_and_store_info(self, ids: tuple[int, ...]) -> None:
        tasks = [GetGalleryinfoUseCase(self.sqlalchemy).execute(id) for id in ids]
        for result in as_completed(tasks):
            result = await result
            await CreateInfoUseCase(self.mongodb).execute(Info.from_galleryinfo(result))

    async def _integrity_check(self, ids: tuple[int, ...]) -> None:
        tasks = [GetGalleryinfoUseCase(self.hitomi_la).execute(id) for id in ids]
        for result in as_completed(tasks):
            try:
                remote_result = await result
                local_result = await GetGalleryinfoUseCase(self.sqlalchemy).execute(
                    remote_result.id
                )
            except GalleryinfoNotFound as e:
                logger.warning(e)
                continue
            diff = DeepDiff(
                remote_result.to_dict(),
                local_result.to_dict(),
                ignore_order=True,
            )
            if diff:
                logger.warning(
                    f"Integrity check failed for ID {remote_result.id}: {diff}"
                )
                await DeleteGalleryinfoUseCase(self.sqlalchemy).execute(
                    remote_result.id
                )
                await DeleteInfoUseCase(self.mongodb).execute(remote_result.id)
                await CreateGalleryinfoUseCase(self.sqlalchemy).execute(remote_result)
                await CreateInfoUseCase(self.mongodb).execute(
                    Info.from_galleryinfo(remote_result)
                )

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
                is_remote=True,
            )
            self.progress.is_mirroring_galleryinfo = False

        local_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
            GetAllInfoIdsUseCase(self.mongodb),
        )

        if local_differences:
            self.progress.is_converting_to_info = True
            await self._process_in_jobs(
                local_differences, self._fetch_and_store_info, is_remote=False
            )
            self.progress.is_converting_to_info = False

            if mirroring_is_end:
                self.progress.last_mirrored = now()

        await self._process_in_jobs(
            remote_differences, self._integrity_check, is_remote=False
        )

    async def start_mirroring(self, delay: float) -> None:
        logger.info(f"Starting Mirroring task with delay: {delay}")
        while True:
            self.progress.last_checked = now()
            async with self._task_lock:
                if not self.progress.is_integrity_checking:
                    await self.mirror()

            await sleep(delay)

    async def start_integrity_check(self, delay: float) -> None:
        logger.info(f"Starting Integrity Check task with delay: {delay}")
        while True:
            await sleep(delay)
            self.progress.last_checked = now()
            async with self._task_lock:
                if (
                    not self.progress.is_mirroring_galleryinfo
                    and not self.progress.is_converting_to_info
                ):
                    self.progress.is_integrity_checking = True
                    await self._process_in_jobs(
                        tuple(await GetAllGalleryinfoIdsUseCase(self.sqlalchemy)),
                        self._integrity_check,
                        is_remote=False,
                    )
                    self.progress.is_integrity_checking = False
