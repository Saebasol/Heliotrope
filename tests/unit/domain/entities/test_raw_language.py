from heliotrope.domain.entities.raw_language import RawLanguage


def test_raw_language_creation():
    raw_language = RawLanguage(
        galleryid=1,
        language_localname="english",
        name="english",
        url="http://example.com",
    )

    assert raw_language.galleryid == 1
    assert raw_language.language_localname == "english"
    assert raw_language.name == "english"
    assert raw_language.url == "http://example.com"


def test_raw_language_serialization():
    raw_language = RawLanguage(
        galleryid=1,
        language_localname="english",
        name="english",
        url="http://example.com",
    )

    assert {
        "galleryid": 1,
        "language_localname": "english",
        "name": "english",
        "url": "http://example.com",
    } == raw_language.to_dict()


def test_raw_language_deserialization():
    raw_language = RawLanguage.from_dict(
        {
            "galleryid": 1,
            "language_localname": "english",
            "name": "english",
            "url": "http://example.com",
        }
    )

    assert raw_language.galleryid == 1
    assert raw_language.language_localname == "english"
    assert raw_language.name == "english"
    assert raw_language.url == "http://example.com"


def test_raw_language_equality():
    raw_language1 = RawLanguage(
        galleryid=1,
        language_localname="english",
        name="english",
        url="http://example.com",
    )

    raw_language2 = RawLanguage(
        galleryid=1,
        language_localname="english",
        name="english",
        url="http://example.com",
    )

    raw_language3 = RawLanguage(
        galleryid=2,
        language_localname="japanese",
        name="japanese",
        url="http://different.com",
    )

    assert raw_language1 == raw_language2
    assert raw_language1 != raw_language3
