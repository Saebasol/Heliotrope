import asyncio

from heliotrope.database.models.hitomi import File, GalleryInfo, Index, Tag
from heliotrope.database.models.requestcount import RequestCount
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel
from heliotrope.utils.useful import remove_id_and_index_id


async def get_all_request_count():
    if rank_list := await RequestCount.all().values():
        sorted_ranking = sorted(rank_list, key=lambda info: info["count"], reverse=True)
        return {
            "total": len(sorted_ranking),
            "list": sorted_ranking,
        }


async def add_request_count(index: int):
    if index_data := await RequestCount.get_or_none(index=index):
        index_data.count += 1
        await index_data.save()
        return True
    elif galleryinfo := await GalleryInfo.get_or_none(id=index):
        index_data = await RequestCount.create(
            index=index, count=1, title=galleryinfo.title
        )
        await index_data.save()
        return True


async def get_galleryinfo(index: int, include_files: bool = True):
    if galleryinfo := await GalleryInfo.get_or_none(id=index):
        galleryinfo_dict = {
            **(await galleryinfo.filter(id=galleryinfo.id).values())[0],
            "tags": remove_id_and_index_id(await galleryinfo.tags.all().values()),
        }
        if include_files:
            galleryinfo_dict.update(
                {
                    "files": remove_id_and_index_id(
                        await galleryinfo.files.all().values()
                    )
                }
            )
        return galleryinfo_dict


async def put_galleryinfo(galleryinfo: HitomiGalleryInfoModel):
    galleyinfo_orm_object = await GalleryInfo.create(
        language_localname=galleryinfo.language_localname,
        language=galleryinfo.language,
        date=galleryinfo.date,
        japanese_title=galleryinfo.japanese_title,
        title=galleryinfo.title,
        id=galleryinfo.galleryid,
        type=galleryinfo.hitomi_type,
    )

    if galleryinfo.files:
        file_orm_object_list = list(
            map(
                lambda file_info: File(
                    index_id=galleryinfo.galleryid,
                    width=file_info.get("width"),
                    hash=file_info.get("hash"),
                    haswebp=file_info.get("haswebp"),
                    name=file_info.get("name"),
                    height=file_info.get("height"),
                ),
                galleryinfo.files,
            )
        )
        await asyncio.gather(
            *list(
                map(
                    lambda file_orm_object: file_orm_object.save(), file_orm_object_list
                )
            )
        )
        await galleyinfo_orm_object.files.add(*file_orm_object_list)

    if galleryinfo.tags:
        tag_orm_object_list = list(
            map(
                lambda tag_info: Tag(
                    index_id=galleryinfo.galleryid,
                    male=tag_info.get("male"),
                    female=tag_info.get("female"),
                    tag=tag_info.get("tag"),
                    url=tag_info.get("url"),
                ),
                galleryinfo.tags,
            )
        )
        await asyncio.gather(
            *list(
                map(lambda tag_orm_object: tag_orm_object.save(), tag_orm_object_list)
            )
        )
        await galleyinfo_orm_object.tags.add(*tag_orm_object_list)


async def put_index(index: int):
    await Index.create(index_id=index)


async def get_index():
    return list(
        map(int, await Index.all().values_list("index_id", flat=True)),
    )


async def get_sorted_index():
    return sorted(await get_index(), reverse=True)


async def search_galleryinfo(
    query: str, offset: int = 0, limit: int = 15, include_files: bool = False
):
    if (count := await GalleryInfo.filter(title__icontains=query).count()) and (
        not 0 == count
    ):
        search_result_list = (
            await GalleryInfo.filter(title__icontains=query).limit(limit).offset(offset)
        )

        parsed_result_list = []
        for search_result in search_result_list:
            parsed_result = {
                **(await search_result.filter(id=search_result.id).values())[0],
                "tags": remove_id_and_index_id(await search_result.tags.all().values()),
            }
            if include_files:
                parsed_result.update(
                    {
                        "files": remove_id_and_index_id(
                            await search_result.files.all().values()
                        )
                    }
                )
            parsed_result_list.append(parsed_result)

        return parsed_result_list, count
