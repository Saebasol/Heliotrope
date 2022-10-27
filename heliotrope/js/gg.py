import re
from decimal import Decimal


class GG:
    def __init__(self, code: str) -> None:
        self.code = code
        self.b = ""
        self.case: list[int] = []
        self.init_o = 0
        self.re_alloc_o = 0

    def parse(self):
        self.case.clear()
        lines = self.code.split("\n")
        for line in lines:
            if line.startswith("var o = ") and line.endswith(";"):
                self.init_o = int(line.removeprefix("var o = ").removesuffix(";"))
            if line.startswith("o = ") and line.endswith("; break;"):
                self.re_alloc_o = int(
                    line.removeprefix("o = ").removesuffix("; break;")
                )
            if line.startswith("case "):
                matched_int = line.removeprefix("case ").removesuffix(":")
                self.case.append(int(matched_int))
            if line.startswith("b: "):
                self.b = line.removeprefix("b: '").removesuffix("'")

    def m(self, g: int) -> int:
        if g in self.case:
            return self.re_alloc_o
        return self.init_o

    def s(self, h: str) -> str:
        m = re.search(r"(..)(.)$", h)
        assert m
        return str(Decimal(int(m[2] + m[1], 16)))
