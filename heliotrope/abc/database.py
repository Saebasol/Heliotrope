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
from abc import ABC, abstractmethod
from typing import Optional

from heliotrope.domain.galleryinfo import Galleryinfo
from heliotrope.domain.info import Info


class AbstractInfoDatabase(ABC):
    info_tags = ["artist", "group", "type", "language", "series", "character"]
    gender_common_tags = ["female", "tags", "male"]

    @abstractmethod
    async def get_all_index(self) -> list[int]:
        """
        Get all index.
        """

    @abstractmethod
    async def add_info(self, info: Info) -> None:
        """
        Add info to the database.
        """

    @abstractmethod
    async def get_info(self, id: int) -> Optional[Info]:
        """
        Get info by id.
        """

    @abstractmethod
    async def get_info_list(
        self, language: Optional[str], offset: int, limit: int
    ) -> list[Info]:
        """
        Get info list.
        """

    @abstractmethod
    async def get_random_info(self, query: list[str]) -> Info:
        """
        Get random info.
        """

    @abstractmethod
    async def search(
        self,
        query: list[str],
        offset: int,
        limit: int,
    ) -> tuple[list[Info], int]:
        """
        Search info by tags.
        """


class AbstractGalleryinfoDatabase(ABC):
    @abstractmethod
    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> None:
        """
        Add galleryinfo to the database.
        """

    @abstractmethod
    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        """
        Get galleryinfo by id.
        """

    @abstractmethod
    async def get_all_index(self) -> list[int]:
        """
        Get all index.
        """
