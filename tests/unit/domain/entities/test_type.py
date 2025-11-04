from yggdrasil.domain.entities.type import Type


def test_type_creation():
    gallery_type = Type(type="doujinshi")
    assert gallery_type.type == "doujinshi"


def test_type_serialization():
    gallery_type = Type(type="doujinshi")
    assert {"type": "doujinshi"} == gallery_type.to_dict()


def test_type_deserialization():
    data = {"type": "doujinshi"}
    gallery_type = Type.from_dict(data)
    assert gallery_type.type == "doujinshi"


def test_type_equality():
    type1 = Type(type="doujinshi")
    type2 = Type(type="doujinshi")
    type3 = Type(type="manga")
    assert type1 == type2
    assert type1 != type3
