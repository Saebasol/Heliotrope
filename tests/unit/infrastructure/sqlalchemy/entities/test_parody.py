from yggdrasil.infrastructure.sqlalchemy.entities.parody import ParodySchema


def test_parody_schema_creation():
    parody = ParodySchema(parody="test parody", url="http://example.com/parody")
    assert parody.parody == "test parody"
    assert parody.url == "http://example.com/parody"


def test_parody_schema_table_name():
    assert ParodySchema.__tablename__ == "parody"


def test_parody_schema_equality():
    parody1 = ParodySchema(parody="test parody", url="http://example.com/parody")
    parody2 = ParodySchema(parody="test parody", url="http://example.com/parody")
    parody3 = ParodySchema(parody="different parody", url="http://example.com/parody")

    assert parody1.parody == parody2.parody
    assert parody1.url == parody2.url
    assert parody1.parody != parody3.parody


def test_parody_schema_attributes():
    parody = ParodySchema(parody="test parody", url="http://example.com/parody")

    # Test that all required attributes exist
    assert hasattr(parody, "parody")
    assert hasattr(parody, "url")
    assert hasattr(parody, "id")  # From Schema base class

    # Test attribute types
    assert isinstance(parody.parody, str)
    assert isinstance(parody.url, str)
