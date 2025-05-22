from asyncio import sleep

from sanic.log import logger

from heliotrope.application.tasks.mirroring import MirroringTask
from heliotrope.application.usecases.get.galleryinfo import GetAllGalleryinfoIdsUseCase


class IntegrityTask(MirroringTask):
    async def start(self, delay: float) -> None:
        logger.info(f"Starting Integrity task with delay: {delay}")
        while True:
            await sleep(delay)
            if (
                not self.progress.is_mirroring_galleryinfo
                or not self.progress.is_converting_to_info
            ):
                self.progress.is_integrity_checking = True

                await self._process_in_jobs(
                    tuple(await GetAllGalleryinfoIdsUseCase(self.sqlalchemy)),
                    self._integrity_check,
                    is_remote=False,
                )

                self.progress.is_integrity_checking = False
