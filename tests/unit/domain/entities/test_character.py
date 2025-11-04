from yggdrasil.domain.entities.character import Character


def test_character_creation():
    character = Character(character="test", url="http://example.com")
    assert character.character == "test"
    assert character.url == "http://example.com"


def test_character_serialization():
    character = Character(character="test", url="http://example.com")
    assert {"character": "test", "url": "http://example.com"} == character.to_dict()


def test_character_deserialization():
    data = {"character": "test", "url": "http://example.com"}
    character = Character.from_dict(data)
    assert character.character == "test"
    assert character.url == "http://example.com"


def test_character_equality():
    character1 = Character(character="test", url="http://example.com")
    character2 = Character(character="test", url="http://example.com")
    character3 = Character(character="different", url="http://example.com")
    assert character1 == character2
    assert character1 != character3
