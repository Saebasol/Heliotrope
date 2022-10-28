import re
from decimal import Decimal


class GG:
    def __init__(self, code: str) -> None:
        self.code = code
        self.case: list[int] = []
        self.default_o = 0
        self.in_case_o = 0

    def parse(self) -> None:
        lines = self.code.split("\n")
        for line in lines:
            if line.startswith("var o = ") and line.endswith(";"):
                self.default_o = int(line.removeprefix("var o = ").removesuffix(";"))
            if line.startswith("o = ") and line.endswith("; break;"):
                self.in_case_o = int(line.removeprefix("o = ").removesuffix("; break;"))
            if line.startswith("case "):
                matched_int = line.removeprefix("case ").removesuffix(":")
                self.case.append(int(matched_int))
            if line.startswith("b: "):
                self.b = line.removeprefix("b: '").removesuffix("'")

    def refresh(self, code: str):
        self.code = code
        self.case.clear()
        self.parse()

    def m(self, g: int) -> int:
        if g in self.case:
            return self.in_case_o
        return self.default_o

    def s(self, h: str) -> str:
        m = re.search(r"(..)(.)$", h)
        assert m
        return str(Decimal(int(m[2] + m[1], 16)))
