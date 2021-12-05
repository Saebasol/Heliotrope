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
from typing import Literal, Optional, TypedDict


class _HitomiFileJSONOptional(TypedDict, total=False):
    hasavifsmalltn: Literal[1]
    hasavif: Literal[1]


class HitomiFileJSON(_HitomiFileJSONOptional):
    width: int
    hash: str
    haswebp: Literal[0, 1]
    name: str
    height: int


class _HitomiTagJSONOptional(TypedDict, total=False):
    male: Optional[Literal["", "1"]]
    female: Optional[Literal["", "1"]]


class HitomiTagJSON(_HitomiTagJSONOptional):
    url: str
    tag: str


class HitomiGalleryinfoJSON(TypedDict):
    date: str
    title: str
    type: str
    japanese_title: Optional[str]
    language: str
    files: list[HitomiFileJSON]
    id: str
    language_localname: str
    tags: list[HitomiTagJSON]


class HitomiInfoJSON(TypedDict):
    id: str
    title: str
    thumbnail: str
    artist: list[str]
    group: list[str]
    type: str
    language: str
    series: list[str]
    character: list[str]
    tags: list[str]
    date: str
