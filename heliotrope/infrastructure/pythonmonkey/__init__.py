from __future__ import annotations

import re

from pythonmonkey import eval  # pyright: ignore[reportMissingTypeStubs]
from sanic.log import logger

from heliotrope.domain.entities.file import File
from heliotrope.infrastructure.hitomila import HitomiLa


class JavaScriptInterpreter:
    def __init__(self, hitomi_la: HitomiLa) -> None:
        self.hitomi_la = hitomi_la
        self.gg_code = ""
        eval(r"var gg = {}")
        eval("var domain2 = 'gold-usergeneratedcontent.net';")

    def image_url_from_image(self, galleryid: int, image: File, no_webp: bool) -> str:
        ext = "webp"
        if image.hasavif and no_webp:
            ext = "avif"

        return self.url_from_url_from_hash(galleryid, image, ext, "", "")

    def url_from_url_from_hash(
        self, galleryid: int, image: File, dir: str, ext: str, base: str
    ) -> str:
        return eval("url_from_url_from_hash")(str(galleryid), image, dir, ext, base)

    def parse_common_js(self, js_code: str) -> str:
        target_functions = [
            "subdomain_from_url",
            "url_from_url",
            "full_path_from_hash",
            "real_full_path_from_hash",
            "url_from_hash",
            "url_from_url_from_hash",
            "rewrite_tn_paths",
        ]

        pattern_start = re.compile(
            rf"function\s+({'|'.join(target_functions)})\s*\([^)]*\)\s*{{"
        )

        functions: list[str] = []
        pos = 0
        while pos < len(js_code):
            match = pattern_start.search(js_code, pos)
            if not match:
                break

            start_pos = match.start()
            brace_count = 0
            i = match.end() - 1  # Starting position of the function body

            # Find the matching closing brace
            while i < len(js_code):
                if js_code[i] == "{":
                    brace_count += 1
                elif js_code[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:  # Found the matching closing brace
                        break
                i += 1

            if i < len(js_code):
                # Extract the entire function text
                function_text = js_code[start_pos : i + 1]
                functions.append(function_text)

            pos = i + 1

        return "\n".join(functions)

    async def get_common_js(self) -> str:
        async with self.hitomi_la.session.get(
            self.hitomi_la.ltn_url.with_path("common.js")
        ) as response:
            return await response.text()

    async def refresh_gg_js(self) -> None:
        gg_code = await self.get_gg_js()
        if self.gg_code != gg_code:
            self.gg_code = gg_code
            eval(self.gg_code)

    async def get_gg_js(self) -> str:
        async with self.hitomi_la.session.get(
            self.hitomi_la.ltn_url.with_path("gg.js")
        ) as response:
            return await response.text()

    async def evaluate_common_js(self) -> None:
        common_js_code = await self.get_common_js()
        to_eval = self.parse_common_js(common_js_code)
        eval(to_eval)

    @classmethod
    async def setup(cls, hitomi_la: HitomiLa) -> JavaScriptInterpreter:
        logger.info("Setting up JavaScript interpreter")
        interpreter = cls(hitomi_la)
        logger.debug("Evaluating common.js")
        await interpreter.evaluate_common_js()
        logger.debug("Initializing gg.js")
        await interpreter.refresh_gg_js()
        return interpreter
