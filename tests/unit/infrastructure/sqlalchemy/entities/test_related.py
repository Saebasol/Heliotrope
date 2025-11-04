from yggdrasil.infrastructure.sqlalchemy.entities.related import RelatedSchema


def test_related_schema_creation():
    related = RelatedSchema(related_id=54321)
    assert related.related_id == 54321


def test_related_schema_table_name():
    assert RelatedSchema.__tablename__ == "related"


def test_related_schema_equality():
    related1 = RelatedSchema(related_id=54321)
    related2 = RelatedSchema(related_id=54321)
    related3 = RelatedSchema(related_id=67890)

    assert related1.related_id == related2.related_id
    assert related1.related_id != related3.related_id


def test_related_schema_attributes():
    related = RelatedSchema(related_id=54321)

    # Test that all required attributes exist
    assert hasattr(related, "related_id")
    assert hasattr(related, "id")  # From ForeignKeySchema base class
    assert hasattr(related, "galleryinfo_id")  # From ForeignKeySchema base class

    # Test attribute types
    assert isinstance(related.related_id, int)
