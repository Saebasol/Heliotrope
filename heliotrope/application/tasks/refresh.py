from asyncio.tasks import sleep
from typing import NoReturn


from heliotrope.application.sanic import Heliotrope


class RefreshggJS:
    def __init__(self, app: Heliotrope) -> None:
        self.app = app

    async def start(self, delay: float) -> NoReturn:
        while True:
            await sleep(delay)
            await self.app.ctx.javascript_interpreter.refresh_gg_js()
