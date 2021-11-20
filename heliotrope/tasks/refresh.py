from asyncio import sleep
from typing import Any, Callable, Coroutine, NoReturn

from heliotrope.hitomi.common import CommonJS


class RefreshCommonJS:
    def __init__(
        self,
        common_js_request_function: Callable[[], Coroutine[Any, Any, str]],
        common_js: CommonJS,
    ) -> None:
        self.common_js = common_js
        self.get = common_js_request_function

    @classmethod
    async def setup(
        cls, common_js_request_function: Callable[[], Coroutine[Any, Any, str]]
    ) -> "RefreshCommonJS":
        common_js = await common_js_request_function()
        return cls(common_js_request_function, CommonJS.setup(common_js))

    async def task(self, delay: float) -> NoReturn:
        while True:
            body = await self.get()

            if self.common_js.get_js_function(body) != self.common_js.body:
                self.common_js.body = self.common_js.get_js_function(body)
                self.common_js.engine.execute(body)

            await sleep(delay)
