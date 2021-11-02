from asyncio import sleep
from typing import Any, Callable, Coroutine, NoReturn

from heliotrope.hitomi.common import CommonJS
from heliotrope.utils.js import (
    get_parsed_functions_from_source,
    make_js_program,
    translate_tree,
)


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
        self = cls(common_js_request_function, CommonJS(common_js))
        return self

    async def task(self, delay: float) -> NoReturn:
        newer: list[dict[str, Any]] = []

        while True:
            common_js = await self.get()
            parsed = get_parsed_functions_from_source(
                common_js, self.common_js.FUNCTIONS
            )

            for origin, remote in zip(self.common_js.body, parsed):
                if origin != remote:
                    newer.append(remote)

            if newer:
                tree = make_js_program(newer)
                pycode = translate_tree(tree, "")
                self.common_js.engine.exec_pycode(pycode)

            newer.clear()

            await sleep(delay)
