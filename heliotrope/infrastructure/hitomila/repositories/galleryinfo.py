from json import loads
from struct import unpack
from typing import Any

from heliotrope.application.dtos.galleryinfo import GalleryinfoDTO
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.repositories.galleryinfo import GalleryinfoRepository
from heliotrope.infrastructure.hitomila import HitomiLa


class HitomiLaGalleryinfoRepository(GalleryinfoRepository):
    def __init__(self, hitomi_la: HitomiLa) -> None:
        self.hitomi_la = hitomi_la

    async def get_galleryinfo(self, id: int) -> Galleryinfo | None:
        request_url = self.hitomi_la.ltn_url.with_path(f"galleries/{id}.js")
        response = await self.hitomi_la.session.get(request_url)

        if response.status != 200:
            return None

        js_to_json = loads(str(await response.text()).replace("var galleryinfo = ", ""))

        return GalleryinfoDTO.from_dict(js_to_json).to_domain()

    async def __fetch_galleryinfo(self, headers: dict[str, Any]) -> list[int]:
        index: list[int] = []
        for request_url in self.hitomi_la.index_url:
            response = await self.hitomi_la.session.get(request_url, headers=headers)
            body = await response.read()
            total_items = len(body) // 4
            index.extend(list(unpack(f">{total_items}i", bytes(body))))
        return index

    async def get_galleryinfo_ids(self, page: int = 1, item: int = 25) -> list[int]:
        byte_start = (page - 1) * item * 4
        byte_end = byte_start + item * 4 - 1
        headers = {
            **self.hitomi_la.headers,
            "Range": f"bytes={byte_start}-{byte_end}",
        }
        return await self.__fetch_galleryinfo(headers=headers)

    async def get_all_galleryinfo_ids(self) -> list[int]:
        return await self.__fetch_galleryinfo(headers=self.hitomi_la.headers)

    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> int:
        raise NotImplementedError

    async def is_galleryinfo_exists(self, id: int) -> bool:
        return await self.get_galleryinfo(id) is not None

    async def delete_galleryinfo(self, id: int) -> None:
        raise NotImplementedError
