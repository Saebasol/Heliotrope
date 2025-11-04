from yggdrasil.application.dtos.list import ListResultDTO
from yggdrasil.domain.entities.info import Info

from tests.unit.domain.entities.conftest import sample_info as sample_info


def test_list_result_dto_creation(sample_info: Info):
    character = ListResultDTO(items=[sample_info], count=1)
    assert character.items[0] == sample_info
    assert character.count == 1


def test_list_result_dto_serialization(sample_info: Info):
    dto = ListResultDTO(items=[sample_info], count=1)
    expected_dict = {"items": [sample_info.to_dict()], "count": 1}
    assert dto.to_dict() == expected_dict
