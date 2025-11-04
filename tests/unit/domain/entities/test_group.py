from yggdrasil.domain.entities.group import Group


def test_group_creation():
    group = Group(group="test", url="http://example.com")
    assert group.group == "test"
    assert group.url == "http://example.com"


def test_group_serialization():
    group = Group(group="test", url="http://example.com")
    assert {"group": "test", "url": "http://example.com"} == group.to_dict()


def test_group_deserialization():
    data = {"group": "test", "url": "http://example.com"}
    group = Group.from_dict(data)
    assert group.group == "test"
    assert group.url == "http://example.com"


def test_group_equality():
    group1 = Group(group="test", url="http://example.com")
    group2 = Group(group="test", url="http://example.com")
    group3 = Group(group="different", url="http://example.com")
    assert group1 == group2
    assert group1 != group3
