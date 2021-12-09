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
from typing import NoReturn
from heliotrope.abc import AbstractTask
from heliotrope.request.hitomi import HitomiRequest
from heliotrope.interpreter import CommonJS
from heliotrope.sanic import Heliotrope
from asyncio.tasks import Task, sleep, create_task

from heliotrope.tasks import HeliotropeTask


@HeliotropeTask.register("REFRESH_COMMON_JS_DELAY")
class RefreshCommonJS(AbstractTask):
    def __init__(self, request: HitomiRequest, common_js: CommonJS) -> None:
        self.request = request
        self.common_js = common_js

    async def start(self, delay: float) -> NoReturn:
        while True:
            if not self.common_js.code:
                self.common_js.update_common_js_code(await self.request.get_common_js())
                await sleep(delay)

            code = await self.request.get_common_js()

            if self.common_js.code != code:
                self.common_js.update_common_js_code(code)
            await sleep(delay)

    @classmethod
    async def setup(cls, app: Heliotrope, delay: float) -> Task[NoReturn]:
        instance = cls(app.ctx.hitomi_request, app.ctx.common_js)
        return create_task(instance.start(delay))
