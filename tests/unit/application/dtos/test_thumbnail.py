from yggdrasil.application.dtos.thumbnail import GetThumbnailQueryDTO, Size


def test_size_enum_values():
    assert Size.SMALLSMALL.value == "smallsmall"
    assert Size.SMALL.value == "small"
    assert Size.SMALLBIG.value == "smallbig"
    assert Size.BIG.value == "big"


def test_get_thumbnail_query_dto_creation():
    dto = GetThumbnailQueryDTO(size=Size.SMALL, single="true")
    assert dto.size == Size.SMALL
    assert dto.single == "true"
