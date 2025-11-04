from yggdrasil.domain.entities.parody import Parody


def test_parody_creation():
    parody = Parody(parody="test", url="http://example.com")
    assert parody.parody == "test"
    assert parody.url == "http://example.com"


def test_parody_serialization():
    parody = Parody(parody="test", url="http://example.com")
    assert {"parody": "test", "url": "http://example.com"} == parody.to_dict()


def test_parody_deserialization():
    data = {"parody": "test", "url": "http://example.com"}
    parody = Parody.from_dict(data)
    assert parody.parody == "test"
    assert parody.url == "http://example.com"


def test_parody_equality():
    parody1 = Parody(parody="test", url="http://example.com")
    parody2 = Parody(parody="test", url="http://example.com")
    parody3 = Parody(parody="different", url="http://example.com")
    assert parody1 == parody2
    assert parody1 != parody3
