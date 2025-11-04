from yggdrasil.infrastructure.sqlalchemy.entities.character import CharacterSchema


def test_character_schema_creation():
    character = CharacterSchema(
        character="test character", url="http://example.com/character"
    )
    assert character.character == "test character"
    assert character.url == "http://example.com/character"


def test_character_schema_serialization():
    character = CharacterSchema(
        character="test character", url="http://example.com/character"
    )
    serialized = character.to_dict()

    assert "character" in serialized
    assert "url" in serialized
    assert serialized["character"] == "test character"
    assert serialized["url"] == "http://example.com/character"


def test_character_schema_deserialization():
    data = {"character": "test character", "url": "http://example.com/character"}
    character = CharacterSchema.from_dict(data)

    assert character.character == "test character"
    assert character.url == "http://example.com/character"


def test_character_schema_equality():
    character1 = CharacterSchema(
        character="test character", url="http://example.com/character"
    )
    character2 = CharacterSchema(
        character="test character", url="http://example.com/character"
    )
    character3 = CharacterSchema(
        character="different character", url="http://example.com/character"
    )

    assert character1 == character2
    assert character1 != character3
