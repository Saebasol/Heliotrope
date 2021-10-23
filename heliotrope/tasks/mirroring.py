from asyncio import sleep
from typing import Any, NoReturn

from aiohttp.client import ClientSession

from heliotrope.database.mongo import NoSQLQuery
from heliotrope.database.query import SQLQuery
from heliotrope.request.hitomi import HitomiRequest


class Mirroring(HitomiRequest):
    def __init__(
        self, sql_query: SQLQuery, nosql_query: NoSQLQuery, session: ClientSession
    ):
        super().__init__(session)
        self.__sql_query = sql_query
        self.__nosql_query = nosql_query

    @classmethod
    async def setup(cls, **kwargs: Any) -> "Mirroring":
        sql_query = kwargs.pop("sql_query")
        nosql_query = kwargs.pop("nosql_query")
        session = ClientSession(**kwargs)
        mirroring = cls(sql_query, nosql_query, session)
        mirroring.session.headers.update(mirroring.headers)
        mirroring.total = len(await mirroring.__sql_query.get_index())
        return mirroring

    async def compare_index_list(self) -> list[int]:
        remote_index_list = await self.fetch_index(include_range=False)
        local_index_list = await self.__sql_query.get_index()
        return list(set(remote_index_list) - set(local_index_list))

    async def mirroring(self, index_list: list[int]) -> None:
        for index in index_list:
            if galleryinfo := await self.get_galleryinfo(index):
                if not await self.__sql_query.get_galleryinfo(index):
                    await self.__sql_query.add_galleryinfo(galleryinfo)

            if info := await self.get_info(index):
                if not await self.__nosql_query.find_info(index):
                    await self.__nosql_query.insert_info(
                        {"index": index, **info.to_dict()}
                    )

            if index not in await self.__sql_query.get_index():
                await self.__sql_query.add_index(index)

    async def task(self, delay: float) -> NoReturn:
        while True:
            if index_list := await self.compare_index_list():
                await self.mirroring(index_list)
                self.total = len(await self.__sql_query.get_index())
            await sleep(delay)
