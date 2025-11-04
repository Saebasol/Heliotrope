from datetime import datetime

from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.domain.entities.info import (
    Info,
    parse_male_female_tag,
    parse_tags_dict_list,
)
from yggdrasil.domain.entities.tag import Tag


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


def test_info_from_galleryinfo(sample_galleryinfo: Galleryinfo):
    info = Info.from_galleryinfo(sample_galleryinfo)

    assert info.id == sample_galleryinfo.id
    assert info.title == sample_galleryinfo.title
    assert info.artists == [
        artist.artist.replace(" ", "_") for artist in sample_galleryinfo.artists
    ]
    assert info.groups == [
        group.group.replace(" ", "_") for group in sample_galleryinfo.groups
    ]
    assert info.type == sample_galleryinfo.type.type
    assert info.language == sample_galleryinfo.language_info.language
    assert info.series == [
        parody.parody.replace(" ", "_") for parody in sample_galleryinfo.parodys
    ]
    assert info.characters == [
        character.character.replace(" ", "_")
        for character in sample_galleryinfo.characters
    ]
    assert info.tags == ["tag:digital"]
    assert info.date == sample_galleryinfo.date


def test_parse_tags_dict_list():
    tags_dict_list = [
        {"tag": "tag1", "url": "http://example.com/tag1"},
        {"tag": "tag 2", "url": "http://example.com/tag2"},
        {"language_url": "http://example.com/lang", "language": "english"},
    ]
    expected = ["tag1", "tag_2", "english"]
    result = parse_tags_dict_list(tags_dict_list)
    assert result == expected


def test_parse_male_female_tag(sample_tag: Tag):
    result = parse_male_female_tag(sample_tag)
    assert result == "tag:digital"


def test_parse_male_female_tag_is_female(sample_tag_female: Tag):
    sample_tag_female.female = True
    result = parse_male_female_tag(sample_tag_female)
    assert result == "female:loli"


def test_parse_male_female_tag_is_male(sample_tag_male: Tag):
    sample_tag_male.male = True
    result = parse_male_female_tag(sample_tag_male)
    assert result == "male:shota"
