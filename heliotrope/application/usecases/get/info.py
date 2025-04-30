from typing import Generator
from heliotrope.application.exceptions import InfoNotFound
from heliotrope.domain.entities.info import Info
from heliotrope.domain.repositories.info import InfoRepository


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

    def __await__(self) -> Generator[None, None, list[int]]:
        return self.execute().__await__()

    async def execute(self) -> list[int]:
        return await self.info_repository.get_all_info_ids()


class GetRandomInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, query: list[str]) -> Info:
        info = await self.info_repository.get_random_info(query)
        if info:
            return info

        raise InfoNotFound


class SearchByQueryUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(
        self, query: list[str], page: int = 0, item: int = 25
    ) -> tuple[int, list[Info]]:
        return await self.info_repository.search_by_query(query, page, item)
