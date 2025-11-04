import pytest
import pytest_asyncio
from yggdrasil.domain.entities.info import Info
from yggdrasil.infrastructure.mongodb import MongoDB
from yggdrasil.infrastructure.mongodb.repositories.info import MongoDBInfoRepository

from tests.unit.domain.entities.conftest import sample_info as sample_info


@pytest_asyncio.fixture()
async def info_repository(mongodb: MongoDB):
    return MongoDBInfoRepository(mongodb)


@pytest.mark.asyncio
async def test_add_info(info_repository: MongoDBInfoRepository, sample_info: Info):
    result_id = await info_repository.add_info(sample_info)

    assert result_id == sample_info.id


@pytest.mark.asyncio
async def test_get_info_existing(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    retrieved_info = await info_repository.get_info(sample_info.id)

    assert retrieved_info is not None
    assert retrieved_info.id == sample_info.id
    assert retrieved_info.title == sample_info.title
    assert retrieved_info.artists == sample_info.artists


@pytest.mark.asyncio
async def test_get_info_non_existing(info_repository: MongoDBInfoRepository):
    retrieved_info = await info_repository.get_info(999999)

    assert retrieved_info is None


@pytest.mark.asyncio
async def test_is_info_exists_true(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    exists = await info_repository.is_info_exists(sample_info.id)

    assert exists is True


@pytest.mark.asyncio
async def test_is_info_exists_false(info_repository: MongoDBInfoRepository):
    exists = await info_repository.is_info_exists(999999)

    assert exists is False


@pytest.mark.asyncio
async def test_get_all_info_ids_with_data(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    info1 = sample_info
    info2 = Info(
        id=123457,
        title="Sample Gallery 2",
        artists=["artist3"],
        groups=[],
        type="doujinshi",
        language="english",
        series=[],
        characters=[],
        tags=["tag3"],
        date=sample_info.date,
    )

    await info_repository.add_info(info1)
    await info_repository.add_info(info2)

    ids = await info_repository.get_all_info_ids()

    assert len(ids) == 2
    assert info1.id in ids
    assert info2.id in ids


@pytest.mark.asyncio
async def test_get_list_info(info_repository: MongoDBInfoRepository, sample_info: Info):
    for i in range(3):
        info = Info(
            id=sample_info.id + i,
            title=f"Sample Gallery {i}",
            artists=[f"artist{i}"],
            groups=[],
            type="manga",
            language="korean",
            series=[],
            characters=[],
            tags=[f"tag{i}"],
            date=sample_info.date,
        )
        await info_repository.add_info(info)

    infos = await info_repository.get_list_info(page=0, item=2)

    assert len(infos) == 2
    assert infos[0].id > infos[1].id


@pytest.mark.asyncio
async def test_delete_info_existing(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    exists_before = await info_repository.is_info_exists(sample_info.id)
    assert exists_before is True

    await info_repository.delete_info(sample_info.id)

    exists_after = await info_repository.is_info_exists(sample_info.id)
    assert exists_after is False


@pytest.mark.asyncio
async def test_search_by_query_title(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    count, infos = await info_repository.search_by_query(["Zenbu"], page=0, item=10)

    assert count == 1
    assert len(infos) == 1
    assert infos[0].id == sample_info.id


@pytest.mark.asyncio
async def test_search_by_query_artist(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    count, infos = await info_repository.search_by_query(
        ["artist:tamano_kedama"], page=0, item=10
    )

    assert count == 1
    assert len(infos) == 1
    assert infos[0].id == sample_info.id


@pytest.mark.asyncio
async def test_search_by_query_no_results(info_repository: MongoDBInfoRepository):
    count, infos = await info_repository.search_by_query(
        ["nonexistent"], page=0, item=10
    )

    assert count == 0
    assert len(infos) == 0


@pytest.mark.asyncio
async def test_get_random_info(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    random_info = await info_repository.get_random_info([])

    assert random_info is not None
    assert random_info.id == sample_info.id


@pytest.mark.asyncio
async def test_get_random_info_with_query(
    info_repository: MongoDBInfoRepository, sample_info: Info
):
    await info_repository.add_info(sample_info)

    random_info = await info_repository.get_random_info(
        [
            "artist:tamano_kedama",
        ]
    )

    assert random_info is not None
    assert random_info.id == sample_info.id


@pytest.mark.asyncio
async def test_get_random_info_no_results(info_repository: MongoDBInfoRepository):
    random_info = await info_repository.get_random_info(["nonexistent"])

    assert random_info is None
