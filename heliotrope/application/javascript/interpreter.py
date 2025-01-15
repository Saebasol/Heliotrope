from pythonmonkey import eval
import re


from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.core.file.domain.entity import File


class JavaScriptInterpreter:
    def __init__(self, hitomi_la: HitomiLa) -> None:
        self.hitomi_la = hitomi_la
        eval(r"var gg = {}")

    def image_urls(
        self, galleryid: int, images: list[File], no_webp: bool
    ) -> list[str]:
        return [
            self.image_url_from_image(galleryid, image, no_webp) for image in images
        ]

    def image_url_from_image(self, galleryid: int, image: File, no_webp: bool) -> str:
        ext = "webp"
        if image.hasavif:
            ext = "avif"

        return self.url_from_url_from_hash(galleryid, image, ext, "", "a")

    def url_from_url_from_hash(
        self, galleryid: int, image: File, dir: str, ext: str, base: str
    ):
        return eval("url_from_url_from_hash")(str(galleryid), image, dir, ext, base)

    def parse_common_js(self, js_code: str):
        target_functions = [
            "subdomain_from_url",
            "url_from_url",
            "full_path_from_hash",
            "real_full_path_from_hash",
            "url_from_hash",
            "url_from_url_from_hash",
            "rewrite_tn_paths",
        ]

        pattern = re.compile(
            rf"""
            (
                function\s+({"|".join(target_functions)})           # "function" 키워드와 함수 이름을 매칭합니다.
                \s*                                                 # 공백 문자(스페이스, 탭 등)가 0개 이상 나올 수 있음을 매칭합니다.
                \(                                                  # 여는 괄호 '('를 매칭합니다.
                [^)]*                                               # 닫는 괄호 ')'가 나오기 전까지의 모든 문자를 매칭합니다 (즉, 함수의 인자 목록).
                \)                                                  # 닫는 괄호 ')'를 매칭합니다.
                \s*                                                 # 공백 문자(스페이스, 탭 등)가 0개 이상 나올 수 있음을 매칭합니다.
                {{                                                  # 여는 중괄호 '{{'를 매칭합니다. 함수 본문 시작.
                (?:                                                 # 비캡처 그룹 시작. 캡처하지 않으면서 내부를 그룹화합니다.
                    [^{{}}]                                         # 여는 중괄호 '{'나 닫는 중괄호 '}'가 아닌 모든 문자를 매칭합니다.
                    |                                               # 또는
                    {{.*?}}                                         # 중첩된 중괄호가 포함된 텍스트를 비탐욕적으로 매칭합니다.
                )*                                                  # 비캡처 그룹의 내용을 0회 이상 반복합니다.
                }}                                                  # 닫는 중괄호 '}}'를 매칭합니다. 함수 본문 끝.
            )
            """,
            re.DOTALL | re.VERBOSE,
        )
        return "\n".join([match[0] for match in pattern.findall(js_code)])

    async def get_common_js(self):
        async with self.hitomi_la.session.get(
            self.hitomi_la.ltn_url.with_path("common.js")
        ) as response:
            return await response.text()

    async def get_gg_js(self):
        async with self.hitomi_la.session.get(
            self.hitomi_la.ltn_url.with_path("gg.js")
        ) as response:
            return await response.text()

    async def evulate_common_js(self):
        common_js_code = await self.get_common_js()
        to_eval = self.parse_common_js(common_js_code)
        eval(to_eval)

    async def evulate_gg_js(self):
        gg_js_code = await self.get_gg_js()
        eval(gg_js_code)

    @classmethod
    async def setup(cls, hitomi_la: HitomiLa):
        interpreter = cls(hitomi_la)
        await interpreter.evulate_common_js()
        await interpreter.evulate_gg_js()
        return interpreter
