from asyncio.tasks import sleep
from typing import NoReturn

from sanic.log import logger

from heliotrope.infrastructure.sanic.app import Heliotrope


class RefreshggJS:
    def __init__(self, app: Heliotrope) -> None:
        self.app = app

    async def start(self, delay: float) -> NoReturn:
        logger.info(f"Starting RefreshggJS task with delay: {delay}")
        while True:
            await sleep(delay)
            await self.app.ctx.pythonmonkey_resolved_image_repository.javascript_interpreter.refresh_gg_js()
