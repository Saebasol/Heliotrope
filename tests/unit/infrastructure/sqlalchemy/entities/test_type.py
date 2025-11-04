from yggdrasil.infrastructure.sqlalchemy.entities.type import TypeSchema


def test_type_schema_creation():
    type_schema = TypeSchema(type="Manga")
    assert type_schema.type == "Manga"


def test_type_schema_equality():
    type1 = TypeSchema(type="Manga")
    type2 = TypeSchema(type="Manga")
    type3 = TypeSchema(type="Doujinshi")

    assert type1.type == type2.type
    assert type1.type != type3.type


def test_type_schema_attributes():
    type_schema = TypeSchema(type="Manga")

    # Test that all required attributes exist
    assert hasattr(type_schema, "type")
    assert hasattr(type_schema, "id")  # From Schema base class

    # Test attribute types
    assert isinstance(type_schema.type, str)
