from heliotrope.domain.exceptions import InfoNotFound
from heliotrope.domain.repositories.info import InfoRepository


class DeleteInfoUseCase:
    def __init__(self, info_repository: InfoRepository) -> None:
        self.info_repository = info_repository

    async def execute(self, id: int) -> None:
        if not await self.info_repository.is_info_exists(id):
            raise InfoNotFound
        await self.info_repository.delete_info(id)
