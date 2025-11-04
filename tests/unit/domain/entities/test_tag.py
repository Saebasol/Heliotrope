from yggdrasil.domain.entities.tag import Tag


def test_tag_creation():
    tag = Tag(tag="test", url="http://example.com")
    assert tag.tag == "test"
    assert tag.url == "http://example.com"
    assert tag.female is False  # default value
    assert tag.male is False  # default value


def test_tag_creation_with_gender():
    female_tag = Tag(tag="test", url="http://example.com", female=True)
    male_tag = Tag(tag="test", url="http://example.com", male=True)

    assert female_tag.female is True
    assert female_tag.male is False
    assert male_tag.female is False
    assert male_tag.male is True


def test_tag_serialization():
    tag = Tag(tag="test", url="http://example.com", female=True, male=False)
    assert {
        "tag": "test",
        "url": "http://example.com",
        "female": True,
        "male": False,
    } == tag.to_dict()


def test_tag_deserialization():
    tag = Tag.from_dict(
        {"tag": "test", "url": "http://example.com", "female": True, "male": False}
    )
    assert tag.tag == "test"
    assert tag.url == "http://example.com"
    assert tag.female is True
    assert tag.male is False


def test_tag_equality():
    tag1 = Tag(tag="test", url="http://example.com", female=True)
    tag2 = Tag(tag="test", url="http://example.com", female=True)
    tag3 = Tag(tag="different", url="http://example.com", male=True)
    assert tag1 == tag2
    assert tag1 != tag3
