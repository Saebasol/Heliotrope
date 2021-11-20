from io import StringIO
from typing import Any, cast

from js2py.evaljs import EvalJs  # type: ignore

from heliotrope.typing import HitomiFilesJSON


class CommonJS:
    FUNCTIONS = [
        "subdomain_from_galleryid",
        "subdomain_from_url",
        "url_from_url",
        "full_path_from_hash",
        "url_from_hash",
        "url_from_url_from_hash",
        "rewrite_tn_paths",
    ]

    @staticmethod
    def get_js_function(code: str):
        functions: list[str] = []
        lines = StringIO(code).readlines()

        finded = False

        for func_name in CommonJS.FUNCTIONS:
            for line in lines:
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

    @classmethod
    def setup(cls, code: str):
        body = cls.get_js_function(code)
        return cls(body)

    def __init__(self, common_js: str) -> None:
        super().__init__()
        self.body = common_js
        self.engine: Any = EvalJs()
        self.engine.execute(common_js)

    def rewrite_tn_paths(self, html: str) -> str:
        return cast(str, self.engine.rewrite_tn_paths(html))

    def image_url_from_image(
        self, galleryid: int, image: HitomiFilesJSON, no_webp: bool
    ) -> str:
        webp = None
        if image["hash"] and image["haswebp"] and not no_webp:
            webp = "webp"

        return cast(str, self.engine.url_from_url_from_hash(galleryid, image, webp))
