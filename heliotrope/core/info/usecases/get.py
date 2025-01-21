from heliotrope.core.info.domain.entity import Info
from heliotrope.core.info.domain.repository import InfoRepository
from heliotrope.core.info.exception import InfoNotFound


class GetInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, id: int) -> Info:
        info = await self.info_repository.get_info(id)

        if info is None:
            raise InfoNotFound

        return info


class GetListInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, page: int = 1, item: int = 25) -> list[Info]:
        return await self.info_repository.get_list_info(page, item)


class GetAllInfoIdsUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    def __await__(self):
        return self.execute().__await__()

    async def execute(self) -> list[int]:
        return await self.info_repository.get_all_info_ids()
