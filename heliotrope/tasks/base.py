from typing import NoReturn


class AbstractTask:
    async def start(self, delay: float) -> NoReturn:
        raise NotImplementedError
