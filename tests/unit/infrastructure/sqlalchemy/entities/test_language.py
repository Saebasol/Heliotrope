from yggdrasil.infrastructure.sqlalchemy.entities.language import LanguageSchema
from yggdrasil.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from yggdrasil.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)


def test_language_schema_creation():
    language = LanguageSchema(
        language_info_id=1,
        localname_id=1,
        galleryid=12345,
        url="http://example.com/language",
        language_info=LanguageInfoSchema(
            id=1, language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(id=1, name="English"),
    )
    assert language.language_info_id == 1
    assert language.localname_id == 1
    assert language.galleryid == 12345
    assert language.url == "http://example.com/language"


def test_language_schema_equality():
    language1 = LanguageSchema(
        id=1,
        language_info_id=1,
        localname_id=1,
        galleryid=12345,
        url="http://example.com/language",
        language_info=LanguageInfoSchema(
            id=1, language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(id=1, name="English"),
    )
    language2 = LanguageSchema(
        id=1,
        language_info_id=1,
        localname_id=1,
        galleryid=12345,
        url="http://example.com/language",
        language_info=LanguageInfoSchema(
            id=1, language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(id=1, name="English"),
    )
    language3 = LanguageSchema(
        id=3,
        language_info_id=1,
        localname_id=1,
        galleryid=12345,
        url="http://example.com/language",
        language_info=LanguageInfoSchema(
            id=1, language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(id=1, name="English"),
    )

    assert language1 == language2
    assert language1 != language3


def test_language_schema_serialization():
    language = LanguageSchema(
        language_info_id=1,
        localname_id=1,
        galleryid=12345,
        url="http://example.com/language",
        language_info=LanguageInfoSchema(
            id=1, language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(id=1, name="English"),
    )
    serialized = language.to_dict()

    assert "galleryid" in serialized
    assert "url" in serialized
    assert serialized["galleryid"] == 12345
    assert serialized["url"] == "http://example.com/language"


def test_language_schema_deserialization():
    data = {
        "language_info_id": 1,
        "localname_id": 1,
        "galleryid": 12345,
        "url": "http://example.com/language",
        "language_info": {
            "id": 1,
            "language": "English",
            "language_url": "http://example.com/language",
        },
        "language_localname": {
            "id": 1,
            "name": "English",
        },
    }
    language = LanguageSchema.from_dict(data)

    assert language.language_info_id == 1
    assert language.localname_id == 1
    assert language.galleryid == 12345
    assert language.url == "http://example.com/language"
