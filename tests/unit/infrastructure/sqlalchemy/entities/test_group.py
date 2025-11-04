from yggdrasil.infrastructure.sqlalchemy.entities.group import GroupSchema


def test_group_schema_creation():
    group = GroupSchema(group="test group", url="http://example.com/group")
    assert group.group == "test group"
    assert group.url == "http://example.com/group"


def test_group_schema_table_name():
    assert GroupSchema.__tablename__ == "group"


def test_group_schema_equality():
    group1 = GroupSchema(group="test group", url="http://example.com/group")
    group2 = GroupSchema(group="test group", url="http://example.com/group")
    group3 = GroupSchema(group="different group", url="http://example.com/group")

    assert group1.group == group2.group
    assert group1.url == group2.url
    assert group1.group != group3.group


def test_group_schema_serialization():
    group = GroupSchema(group="test group", url="http://example.com/group")
    serialized = group.to_dict()

    assert "group" in serialized
    assert "url" in serialized
    assert serialized["group"] == "test group"
    assert serialized["url"] == "http://example.com/group"


def test_group_schema_deserialization():
    data = {"group": "test group", "url": "http://example.com/group"}
    group = GroupSchema.from_dict(data)

    assert group.group == "test group"
    assert group.url == "http://example.com/group"
