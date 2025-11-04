from yggdrasil.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)


def test_language_localname_schema_creation():
    language_localname = LanguageLocalnameSchema(name="English")
    assert language_localname.name == "English"


def test_language_localname_schema_equality():
    language_localname1 = LanguageLocalnameSchema(name="English")
    language_localname2 = LanguageLocalnameSchema(name="English")
    language_localname3 = LanguageLocalnameSchema(name="Japanese")

    assert language_localname1.name == language_localname2.name
    assert language_localname1.name != language_localname3.name


def test_language_localname_schema_attributes():
    language_localname = LanguageLocalnameSchema(name="English")

    # Test that all required attributes exist
    assert hasattr(language_localname, "name")
    assert hasattr(language_localname, "id")  # From Schema base class

    # Test attribute types
    assert isinstance(language_localname.name, str)


def test_language_localname_schema_serialization():
    language_localname = LanguageLocalnameSchema(name="English", id=1)
    serialized = language_localname.to_dict()
    assert serialized == {"name": "English"}


def test_language_localname_schema_deserialization():
    data = {"id": 1, "name": "English"}
    language_localname = LanguageLocalnameSchema.from_dict(data)
    assert language_localname.id == 1
    assert language_localname.name == "English"
