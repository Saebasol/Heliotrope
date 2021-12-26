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
from asyncio.threads import to_thread
from io import StringIO
from typing import cast

from js2py.evaljs import EvalJs  # type: ignore
from sanic.log import logger

from heliotrope.request.hitomi import HitomiRequest
from heliotrope.types import HitomiFileJSON


class CommonJS:
    def __init__(self, polyfill: str) -> None:
        self.interpreter = EvalJs()
        self.polyfill = polyfill
        self.code = ""

    @classmethod
    async def setup(cls, request: HitomiRequest) -> "CommonJS":
        logger.debug(f"Setting up {cls.__name__}")
        common_js_code = await request.get_common_js()
        # Because it is executed only once for the first time, it is safe to block
        with open("./heliotrope/interpreter/polyfill.js") as f:
            polyfill = f.read()
        instance = cls(polyfill)
        instance.update_common_js_code(common_js_code)
        return instance

    def get_using_functions(self, code: str) -> str:
        export_functions_name = [
            "subdomain_from_galleryid",
            "subdomain_from_url",
            "url_from_url",
            "full_path_from_hash",
            "real_full_path_from_hash",
            "url_from_hash",
            "url_from_url_from_hash",
            "rewrite_tn_paths",
        ]
        functions: list[str] = []
        lines = StringIO(code).readlines()

        finded = False
        functions.append(self.polyfill)
        for func_name in export_functions_name:
            for line in lines:
                if line.startswith("var gg"):
                    functions.append(line)
                    continue
                if finded:
                    functions.append(line)
                    if line.startswith("}"):
                        finded = False
                        continue
                if line.startswith(f"function {func_name}"):
                    functions.append(line)
                    finded = True
                    continue

        return "".join(functions)

    def update_common_js_code(self, common_js_code: str) -> None:
        self.code = common_js_code
        self.interpreter.execute(self.get_using_functions(common_js_code))

    async def rewrite_tn_paths(self, html: str) -> str:
        return cast(str, await to_thread(self.interpreter.rewrite_tn_paths, html))

    async def image_url_from_image(
        self, galleryid: int, image: HitomiFileJSON, no_webp: bool
    ) -> str:
        webp = None
        if image["hash"] and image["haswebp"] and not no_webp:
            webp = "webp"

        return cast(
            str,
            await to_thread(
                self.interpreter.url_from_url_from_hash, galleryid, image, webp
            ),
        )
