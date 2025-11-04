from yggdrasil.infrastructure.sqlalchemy.entities.tag import TagSchema


def test_tag_schema_creation():
    tag = TagSchema(tag="test tag", url="http://example.com/tag")
    assert tag.tag == "test tag"
    assert tag.url == "http://example.com/tag"
    assert tag.female is False  # default value
    assert tag.male is False  # default value


def test_tag_schema_creation_with_gender():
    tag = TagSchema(
        tag="test tag", url="http://example.com/tag", female=True, male=False
    )
    assert tag.tag == "test tag"
    assert tag.url == "http://example.com/tag"
    assert tag.female is True
    assert tag.male is False


def test_tag_schema_serialization():
    tag = TagSchema(
        tag="test tag", url="http://example.com/tag", female=True, male=False
    )
    serialized = tag.to_dict()

    assert "tag" in serialized
    assert "url" in serialized
    assert "female" in serialized
    assert "male" in serialized
    assert serialized["tag"] == "test tag"
    assert serialized["url"] == "http://example.com/tag"
    assert serialized["female"] is True
    assert serialized["male"] is False


def test_tag_schema_deserialization():
    data = {
        "tag": "test tag",
        "url": "http://example.com/tag",
        "female": True,
        "male": False,
    }
    tag = TagSchema.from_dict(data)

    assert tag.tag == "test tag"
    assert tag.url == "http://example.com/tag"
    assert tag.female is True
    assert tag.male is False


def test_tag_schema_table_name():
    assert TagSchema.__tablename__ == "tag"


def test_tag_schema_equality():
    tag1 = TagSchema(tag="test tag", url="http://example.com/tag")
    tag2 = TagSchema(tag="test tag", url="http://example.com/tag")
    tag3 = TagSchema(tag="different tag", url="http://example.com/tag")

    assert tag1 == tag2
    assert tag1 != tag3


def test_tag_schema_unique_constraint():
    # Test that the unique constraint exists
    assert hasattr(TagSchema, "__table_args__")
    # The unique constraint should be on tag, female, male columns
    unique_constraint = TagSchema.__table_args__[0]
    assert "tag" in str(unique_constraint)
    assert "female" in str(unique_constraint)
    assert "male" in str(unique_constraint)
