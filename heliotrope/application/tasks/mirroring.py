from asyncio import gather
from heliotrope.infrastructure.hitomila.galleryinfo.domain.repository import (
    HitomiLaGalleryinfoRepository,
)
from heliotrope.infrastructure.sqlalchemy.galleryinfo.domain.repository import (
    SAGalleryinfoRepository,
)
from heliotrope.core.galleryinfo.usecases.get import GetAllGalleryinfoIdsUseCase
from heliotrope.core.galleryinfo.usecases.get import GetGalleryinfoUseCase
from heliotrope.core.galleryinfo.usecases.add import BulkAddGalleryinfoUseCase
from tqdm.asyncio import tqdm


class MirroringTask:
    def __init__(
        self,
        hitomi_la: HitomiLaGalleryinfoRepository,
        sqlalchemy: SAGalleryinfoRepository,
    ) -> None:
        self.hitomi_la = hitomi_la
        self.sqlalchemy = sqlalchemy

    async def compare_local_and_remote(self) -> list[int]:
        remote = await GetAllGalleryinfoIdsUseCase(self.hitomi_la)
        local = await GetAllGalleryinfoIdsUseCase(self.sqlalchemy)

        compared = set(remote) - set(local)

        return list(compared)

    async def process_concurrent(self, concurrent: list[int]):
        tasks = [GetGalleryinfoUseCase(self.hitomi_la).execute(id) for id in concurrent]
        results = await gather(*tasks)
        await BulkAddGalleryinfoUseCase(self.sqlalchemy).execute(results)

    async def mirror(self) -> None:
        compared = await self.compare_local_and_remote()

        if not compared:
            return

        concurrent_size = 100
        concurrents = [
            compared[i : i + concurrent_size]
            for i in range(0, len(compared), concurrent_size)
        ]

        for concurrent in tqdm(concurrents):
            await self.process_concurrent(concurrent)
