from yggdrasil.domain.entities.language_localname import LanguageLocalname


def test_language_localname_creation():
    language_localname = LanguageLocalname(name="english")
    assert language_localname.name == "english"


def test_language_localname_serialization():
    language_localname = LanguageLocalname(name="english")
    assert {"name": "english"} == language_localname.to_dict()


def test_language_localname_deserialization():
    data = {"name": "english"}
    language_localname = LanguageLocalname.from_dict(data)
    assert language_localname.name == "english"


def test_language_localname_equality():
    language_localname1 = LanguageLocalname(name="english")
    language_localname2 = LanguageLocalname(name="english")
    language_localname3 = LanguageLocalname(name="japanese")
    assert language_localname1 == language_localname2
    assert language_localname1 != language_localname3
