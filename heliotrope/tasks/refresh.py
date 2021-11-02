from asyncio import sleep
from typing import Any, Callable, Coroutine, NoReturn

from heliotrope.hitomi.common import CommonJS
from heliotrope.utils.js import (
    get_parsed_functions_from_source,
    make_js_program,
    translate_tree,
)


class RefreshCommonJS:
    common_js_object: CommonJS

    def __init__(
        self, common_js_request_function: Callable[[], Coroutine[Any, Any, str]]
    ) -> None:
        self.get = common_js_request_function

    async def task(self, delay: float) -> NoReturn:
        common_js = await self.get()
        self.common_js_object = CommonJS(common_js)

        newer: list[dict[str, Any]] = []

        while True:
            common_js = await self.get()
            parsed = get_parsed_functions_from_source(
                common_js, self.common_js_object.FUNCTIONS
            )

            for origin, remote in zip(self.common_js_object.body, parsed):
                if origin != remote:
                    newer.append(remote)

            if newer:
                tree = make_js_program(newer)
                pycode = translate_tree(tree, "")
                self.common_js_object.engine.exec_pycode(pycode)

            newer.clear()

            await sleep(delay)
