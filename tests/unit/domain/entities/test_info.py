from datetime import datetime

from heliotrope.domain.entities.info import Info


def test_info_creation():
    info = Info(
        id=1,
        title="Test Gallery",
        artists=["artist1", "artist2"],
        groups=["group1"],
        type="doujinshi",
        language="english",
        series=["series1"],
        characters=["character1"],
        tags=["tag1", "tag2"],
        date=datetime(2023, 1, 1, 12, 0, 0),
    )

    assert info.id == 1
    assert info.title == "Test Gallery"
    assert info.artists == ["artist1", "artist2"]
    assert info.groups == ["group1"]
    assert info.type == "doujinshi"
    assert info.language == "english"
    assert info.series == ["series1"]
    assert info.characters == ["character1"]
    assert info.tags == ["tag1", "tag2"]
    assert info.date == datetime(2023, 1, 1, 12, 0, 0)


def test_info_serialization():
    info = Info(
        id=1,
        title="Test Gallery",
        artists=["artist1", "artist2"],
        groups=["group1"],
        type="doujinshi",
        language="english",
        series=["series1"],
        characters=["character1"],
        tags=["tag1", "tag2"],
        date=datetime(2023, 1, 1, 12, 0, 0),
    )

    result = info.to_dict()

    assert result["id"] == 1
    assert result["title"] == "Test Gallery"
    assert result["artists"] == ["artist1", "artist2"]
    assert result["groups"] == ["group1"]
    assert result["type"] == "doujinshi"
    assert result["language"] == "english"
    assert result["series"] == ["series1"]
    assert result["characters"] == ["character1"]
    assert result["tags"] == ["tag1", "tag2"]


def test_info_deserialization():
    info = Info.from_dict(
        {
            "id": 1,
            "title": "Test Gallery",
            "artists": ["artist1", "artist2"],
            "groups": ["group1"],
            "type": "doujinshi",
            "language": "english",
            "series": ["series1"],
            "characters": ["character1"],
            "tags": ["tag1", "tag2"],
            "date": "2023-01-01T12:00:00",
        }
    )

    assert info.id == 1
    assert info.title == "Test Gallery"
    assert info.artists == ["artist1", "artist2"]
    assert info.groups == ["group1"]
    assert info.type == "doujinshi"
    assert info.language == "english"
    assert info.series == ["series1"]
    assert info.characters == ["character1"]
    assert info.tags == ["tag1", "tag2"]


def test_info_equality():
    info1 = Info(
        id=1,
        title="Test Gallery",
        artists=["artist1"],
        groups=["group1"],
        type="doujinshi",
        language="english",
        series=["series1"],
        characters=["character1"],
        tags=["tag1"],
        date=datetime(2023, 1, 1, 12, 0, 0),
    )

    info2 = Info(
        id=1,
        title="Test Gallery",
        artists=["artist1"],
        groups=["group1"],
        type="doujinshi",
        language="english",
        series=["series1"],
        characters=["character1"],
        tags=["tag1"],
        date=datetime(2023, 1, 1, 12, 0, 0),
    )

    info3 = Info(
        id=2,
        title="Different Gallery",
        artists=["artist2"],
        groups=["group2"],
        type="manga",
        language="japanese",
        series=["series2"],
        characters=["character2"],
        tags=["tag2"],
        date=datetime(2023, 1, 2, 12, 0, 0),
    )

    assert info1 == info2
    assert info1 != info3
