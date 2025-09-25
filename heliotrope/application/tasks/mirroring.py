import math
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
    def __init__(self, status_dict: dict[str, Any]) -> None:
        self.status_dict = status_dict

    def reset(self) -> None:
        self.batch_completed = 0
        self.total_items = 0
        self.batch_total = 0

    def __getattr__(self, name: str) -> Any:
        if name in self.status_dict:
            return self.status_dict[name]

        return super().__getattr__(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAttributeAccessIssue]
            name
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "status_dict":
            super().__setattr__(name, value)
        else:
            self.status_dict[name] = value


@dataclass
class MirroringStatus(Serializer):
    index_files: list[str]
    total_items: int
    batch_total: int
    batch_completed: int
    items_processed: int
    is_mirroring_galleryinfo: bool
    is_converting_to_info: bool
    is_checking_integrity: bool
    last_checked_at: str
    last_mirrored_at: str

    def reset(self) -> None:
        self.batch_completed = 0
        self.total_items = 0
        self.batch_total = 0

    @classmethod
    def default(cls) -> "MirroringStatus":
        return cls(
            index_files=[],
            total_items=0,
            batch_total=0,
            batch_completed=0,
            items_processed=0,
            is_mirroring_galleryinfo=False,
            is_converting_to_info=False,
            is_checking_integrity=False,
            last_checked_at="",
            last_mirrored_at="",
        )


class MirroringTask:
    REMOTE_CONCURRENT_SIZE: int = 50
    LOCAL_CONCURRENT_SIZE: int = 25

    def __init__(
        self,
        hitomi_la_repo: HitomiLaGalleryinfoRepository,
        sqlalchemy_repo: SAGalleryinfoRepository,
        mongodb_repo: MongoDBInfoRepository,
        mirroring_status_dict: dict[str, Any],
    ) -> None:
        self.hitomi_la = hitomi_la_repo
        self.sqlalchemy = sqlalchemy_repo
        self.mongodb = mongodb_repo
        self.status = cast(MirroringStatus, Proxy(mirroring_status_dict))
        self.status.index_files = hitomi_la_repo.hitomi_la.index_files
        self._task_lock = Lock()
        self.skip_ids: set[int] = set()

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
        self.status.total_items = len(ids)
        self.status.batch_total = math.ceil(len(ids) / size)

        for job in self._get_splited_id(ids, size):
            await process_function(job)
            self.status.batch_completed += 1

        self.status.reset()
        self.status.items_processed = len(ids)

    async def _fetch_and_store_galleryinfo(
        self, ids: tuple[int, ...], target_repository: SAGalleryinfoRepository
    ) -> None:
        tasks = [
            self._preprocess(GetGalleryinfoUseCase(self.hitomi_la).execute, id)
            for id in ids
        ]
        async for result in as_completed(tasks):
            result = await result
            await CreateGalleryinfoUseCase(target_repository).execute(result)

    async def _fetch_and_store_info(self, ids: tuple[int, ...]) -> None:
        tasks = [GetGalleryinfoUseCase(self.sqlalchemy).execute(id) for id in ids]
        async for result in as_completed(tasks):
            result = await result
            await CreateInfoUseCase(self.mongodb).execute(Info.from_galleryinfo(result))

    async def _integrity_check(self, ids: tuple[int, ...]) -> None:
        async def __safety(id: int) -> Galleryinfo | None:
            try:
                return await self._preprocess(
                    GetGalleryinfoUseCase(self.hitomi_la).execute, id
                )
            except GalleryinfoNotFound:
                logger.warning(
                    f"Galleryinfo with ID {id} not found remotely. Maybe deleted?"
                    " I'll skip it and not check it next time."
                )
                self.skip_ids.add(id)

        tasks = [__safety(id) for id in ids]
        async for result in as_completed(tasks):
            remote_result = await result
            if remote_result is None:
                continue
            local_result = await GetGalleryinfoUseCase(self.sqlalchemy).execute(
                remote_result.id
            )
            diff = DeepDiff(
                local_result.to_dict(),
                remote_result.to_dict(),
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
            self.status.is_mirroring_galleryinfo = True
            await self._process_in_jobs(
                remote_differences,
                lambda batch: self._fetch_and_store_galleryinfo(batch, self.sqlalchemy),
                is_remote=True,
            )
            self.status.is_mirroring_galleryinfo = False

        local_differences = await self._get_differences(
            GetAllGalleryinfoIdsUseCase(self.sqlalchemy),
            GetAllInfoIdsUseCase(self.mongodb),
        )

        if local_differences:
            self.status.is_converting_to_info = True
            await self._process_in_jobs(
                local_differences, self._fetch_and_store_info, is_remote=False
            )
            self.status.is_converting_to_info = False

            if mirroring_is_end:
                self.status.last_mirrored_at = now()

        await self._process_in_jobs(
            local_differences, self._integrity_check, is_remote=False
        )

    async def start_mirroring(self, delay: float) -> None:
        logger.info(f"Starting Mirroring task with delay: {delay}")
        while True:
            self.status.last_checked_at = now()
            async with self._task_lock:
                if not self.status.is_checking_integrity:
                    try:
                        await self.mirror()
                    finally:
                        self.status.is_converting_to_info = False
                        self.status.is_mirroring_galleryinfo = False
                        self.status.reset()

            await sleep(delay)

    async def start_integrity_check(self, delay: float) -> None:
        logger.info(f"Starting Integrity Check task with delay: {delay}")
        while True:
            await sleep(delay)
            self.status.last_checked_at = now()
            async with self._task_lock:
                if (
                    not self.status.is_mirroring_galleryinfo
                    and not self.status.is_converting_to_info
                ):
                    self.status.is_checking_integrity = True
                    try:
                        await self._process_in_jobs(
                            tuple(
                                set(await GetAllGalleryinfoIdsUseCase(self.sqlalchemy))
                                - self.skip_ids
                            ),
                            self._integrity_check,
                            is_remote=False,
                        )
                    except:
                        self.skip_ids.clear()
                    finally:
                        self.status.is_checking_integrity = False
                        self.status.reset()
