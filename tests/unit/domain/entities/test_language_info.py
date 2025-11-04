from yggdrasil.domain.entities.language_info import LanguageInfo


def test_language_info_creation():
    language_info = LanguageInfo(language="english", language_url="http://example.com")
    assert language_info.language == "english"
    assert language_info.language_url == "http://example.com"


def test_language_info_serialization():
    language_info = LanguageInfo(language="english", language_url="http://example.com")
    assert {
        "language": "english",
        "language_url": "http://example.com",
    } == language_info.to_dict()


def test_language_info_deserialization():
    data = {"language": "english", "language_url": "http://example.com"}
    language_info = LanguageInfo.from_dict(data)
    assert language_info.language == "english"
    assert language_info.language_url == "http://example.com"


def test_language_info_equality():
    language_info1 = LanguageInfo(language="english", language_url="http://example.com")
    language_info2 = LanguageInfo(language="english", language_url="http://example.com")
    language_info3 = LanguageInfo(
        language="japanese", language_url="http://example.com"
    )
    assert language_info1 == language_info2
    assert language_info1 != language_info3
