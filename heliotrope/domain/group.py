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
from typing import Optional

from heliotrope.types import HitomiGroupsJSON


@dataclass
class Group:
    galleryinfo_id: int
    group: str
    url: str
    id: Optional[int] = None

    def to_dict(self) -> HitomiGroupsJSON:
        return HitomiGroupsJSON(
            group=self.group,
            url=self.url,
        )

    @classmethod
    def from_dict(cls, galleryinfo_id: int, d: HitomiGroupsJSON) -> "Group":
        return cls(
            galleryinfo_id=galleryinfo_id,
            group=d["group"],
            url=d["url"],
        )
