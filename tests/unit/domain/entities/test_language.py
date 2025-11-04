from yggdrasil.domain.entities.language import Language
from yggdrasil.domain.entities.language_info import LanguageInfo
from yggdrasil.domain.entities.language_localname import LanguageLocalname


def test_language_creation():
    language_info = LanguageInfo(language="english", language_url="https://example.com")
    language_localname = LanguageLocalname(name="english")

    language = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    assert language.galleryid == 1
    assert language.url == "http://example.com"
    assert isinstance(language.language_localname, LanguageLocalname)
    assert isinstance(language.language_info, LanguageInfo)


def test_language_serialization():
    language_info = LanguageInfo(language="english", language_url="https://example.com")
    language_localname = LanguageLocalname(name="english")

    language = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    result = language.to_dict()

    assert result["galleryid"] == 1
    assert result["url"] == "http://example.com"
    assert "language_localname" in result
    assert "language_info" in result


def test_language_deserialization():
    language = Language.from_dict(
        {
            "galleryid": 1,
            "url": "http://example.com",
            "language_localname": {
                "name": "english",
            },
            "language_info": {
                "language": "english",
                "language_url": "https://example.com",
            },
        }
    )

    assert language.galleryid == 1
    assert language.url == "http://example.com"
    assert isinstance(language.language_localname, LanguageLocalname)
    assert isinstance(language.language_info, LanguageInfo)


def test_language_equality():
    language_info = LanguageInfo(language="english", language_url="https://example.com")
    language_localname = LanguageLocalname(name="english")

    language1 = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    language2 = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    language3 = Language(
        galleryid=2,
        url="http://different.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    assert language1 == language2
    assert language1 != language3
