from heliotrope.domain.entities.info import Info
from heliotrope.domain.repositories.info import InfoRepository


class CreateInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, info: Info) -> None:
        await self.info_repository.add_info(info)
