from yggdrasil.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)


def test_language_info_schema_creation():
    language_info = LanguageInfoSchema(
        language="English", language_url="http://example.com/language"
    )
    assert language_info.language == "English"
    assert language_info.language_url == "http://example.com/language"


def test_language_info_schema_equality():
    language_info1 = LanguageInfoSchema(
        language="English", language_url="http://example.com/language"
    )
    language_info2 = LanguageInfoSchema(
        language="English", language_url="http://example.com/language"
    )
    language_info3 = LanguageInfoSchema(
        language="Japanese", language_url="http://example.com/language/jp"
    )

    assert language_info1.language == language_info2.language
    assert language_info1.language_url == language_info2.language_url
    assert language_info1.language != language_info3.language


def test_language_info_schema_serialization():
    language_info = LanguageInfoSchema(
        language="English", language_url="http://example.com/language"
    )
    serialized = language_info.to_dict()

    assert "language" in serialized
    assert "language_url" in serialized
    assert serialized["language"] == "English"
    assert serialized["language_url"] == "http://example.com/language"


def test_language_info_schema_deserialization():
    data = {"language": "English", "language_url": "http://example.com/language"}
    language_info = LanguageInfoSchema.from_dict(data)

    assert language_info.language == "English"
    assert language_info.language_url == "http://example.com/language"
