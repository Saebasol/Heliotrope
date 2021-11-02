from typing import cast
from heliotrope.typing import HitomiFilesJSON
from heliotrope.utils.js import (
    ExtendEvalJS,
    get_parsed_functions_from_source,
    make_js_program,
    translate_tree,
)


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

    def __init__(self, common_js: str) -> None:
        self.engine = ExtendEvalJS()
        self.body = get_parsed_functions_from_source(common_js, self.FUNCTIONS)
        tree = make_js_program(self.body)
        pycode = translate_tree(tree, "")
        self.engine.exec_pycode(pycode)

    def rewrite_tn_paths(self, html: str) -> str:
        return cast(str, self.engine.rewrite_tn_paths(html))

    def image_url_from_image(
        self, galleryid: int, image: HitomiFilesJSON, no_webp: bool
    ) -> str:
        webp = None
        if image["hash"] and image["haswebp"] and not no_webp:
            webp = "webp"

        return cast(str, self.engine.url_from_url_from_hash(galleryid, image, webp))
