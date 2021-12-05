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
from dataclasses import dataclass
from typing import Literal, Optional

from heliotrope.types import HitomiFileJSON


@dataclass
class File:
    index_id: int
    name: str
    width: int
    height: int
    hash: str
    haswebp: Literal[0, 1]
    hasavifsmalltn: Optional[Literal[1]] = None
    hasavif: Optional[Literal[1]] = None
    id: Optional[int] = None

    def to_dict(self) -> HitomiFileJSON:
        hitomi_file_json = HitomiFileJSON(
            width=self.width,
            hash=self.hash,
            haswebp=self.haswebp,
            name=self.name,
            height=self.height,
        )
        if self.hasavif is not None:
            hitomi_file_json["hasavif"] = self.hasavif

        if self.hasavifsmalltn is not None:
            hitomi_file_json["hasavifsmalltn"] = self.hasavifsmalltn

        return hitomi_file_json

    @classmethod
    def from_dict(cls, index_id: int, d: HitomiFileJSON) -> "File":
        return cls(
            index_id=index_id,
            name=d["name"],
            width=d["width"],
            height=d["height"],
            hash=d["hash"],
            haswebp=d["haswebp"],
            hasavifsmalltn=d.get("hasavifsmalltn"),
            hasavif=d.get("hasavif"),
        )
