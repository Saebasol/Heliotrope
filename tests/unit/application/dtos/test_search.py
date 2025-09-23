from heliotrope.application.dtos.search import (
    PostSearchBodyDTO,
    PostSearchQueryDTO,
    SearchResultDTO,
)
from heliotrope.domain.entities.info import Info
from tests.unit.domain.entities.conftest import sample_info as sample_info


def test_post_search_query_dto_creation():
    query_dto = PostSearchQueryDTO(offset=10)
    assert query_dto.offset == 10


def test_post_search_body_dto_creation():
    body_dto = PostSearchBodyDTO(query=["tag:example"])
    assert body_dto.query == ["tag:example"]


def test_search_result_dto_creation(sample_info: Info):
    search_result_dto = SearchResultDTO(result=[sample_info], count=1)
    assert search_result_dto.result[0] == sample_info
    assert search_result_dto.count == 1


def test_search_result_dto_serialization(sample_info: Info):
    dto = SearchResultDTO(result=[sample_info], count=1)
    expected_dict = {"result": [sample_info.to_dict()], "count": 1}
    assert dto.to_dict() == expected_dict
