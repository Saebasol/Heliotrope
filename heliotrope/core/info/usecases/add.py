from heliotrope.core.info.domain.entity import Info
from heliotrope.core.info.domain.repository import InfoRepository


class AddInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, info: Info) -> None:
        await self.info_repository.add_info(info)


class BulkAddInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, infos: list[Info]) -> None:
        await self.info_repository.bulk_add_info(infos)
