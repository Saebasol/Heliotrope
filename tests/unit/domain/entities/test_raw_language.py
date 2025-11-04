from yggdrasil.domain.entities.language import Language
from yggdrasil.domain.entities.raw_language import RawLanguage


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


def test_raw_language_from_language(sample_language: Language):
    raw_language = RawLanguage.from_language(sample_language)

    assert raw_language.galleryid == sample_language.galleryid
    assert raw_language.language_localname == sample_language.language_localname.name
    assert raw_language.name == sample_language.language_info.language
    assert raw_language.url == sample_language.url


def test_raw_language_to_language(sample_raw_language: RawLanguage):
    language = sample_raw_language.to_language()

    assert language.galleryid == sample_raw_language.galleryid
    assert language.language_localname.name == sample_raw_language.language_localname
    assert language.language_info.language == sample_raw_language.name
    assert language.url == sample_raw_language.url
