"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from asyncio import create_task
from asyncio.tasks import sleep
from typing import NoReturn

from sanic.log import logger

from heliotrope.abc.task import AbstractTask
from heliotrope.js.common import Common
from heliotrope.sanic import Heliotrope
from heliotrope.types import SetupTask

# Sometimes the method of getting the image address may change.
# It resolves this dynamically.

# 때로 이미지 주소를 가져오는 방법이 바뀔수도 있습니다.
# 이를 동적으로 해결합니다.


class RefreshCommonJS(AbstractTask):
    def __init__(self, app: Heliotrope) -> None:
        self.app = app
        self.common_js_code = ""

    async def start(self, delay: float) -> NoReturn:
        while True:
            await sleep(delay)
            renew = await self.app.ctx.hitomi_request.get_gg_js()
            if self.app.ctx.common.gg.code != renew:
                logger.warning("local common js code is different from remote")
                logger.info("Update common js code")
                self.app.ctx.common = Common.setup(renew)

    @classmethod
    def setup(cls, app: Heliotrope, delay: float) -> SetupTask:
        logger.debug(f"Setting up {cls.__name__}")
        instance = cls(app)
        return create_task(instance.start(delay))
