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
from asyncio.tasks import sleep
from typing import NoReturn

from sanic.log import logger

from heliotrope.abc.task import AbstractTask
from heliotrope.interpreter import CommonJS
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.sanic import Heliotrope
from heliotrope.types import SetupTask


class RefreshCommonJS(AbstractTask):
    def __init__(self, request: HitomiRequest, common_js: CommonJS) -> None:
        self.request = request
        self.common_js = common_js

    async def start(self, delay: float) -> NoReturn:
        while True:
            if not self.common_js.common_js_code:
                logger.warning("Common js code is empty")
                logger.info("Update common js code and gg js")
                self.common_js.update_js_code(
                    await self.request.get_common_js(), await self.request.get_gg_js()
                )
                await sleep(delay)

            common_js_code = await self.request.get_common_js()
            gg_js_code = await self.request.get_gg_js()

            if (
                self.common_js.common_js_code != common_js_code
                or self.common_js.gg_js_code != gg_js_code
            ):
                logger.warning("local common js code is different from remote")
                logger.info("Update common js code")
                self.common_js.update_js_code(common_js_code, gg_js_code)
            await sleep(delay)

    @classmethod
    def setup(cls, app: Heliotrope, delay: float) -> SetupTask:
        logger.debug(f"Setting up {cls.__name__}")
        instance = cls(app.ctx.hitomi_request, app.ctx.common_js)
        return instance.start(delay)
