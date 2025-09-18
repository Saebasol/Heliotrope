from datetime import date, datetime

from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.entities.character import Character
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.group import Group
from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.entities.raw_galleryinfo import RawGalleryinfo
from heliotrope.domain.entities.raw_language import RawLanguage
from heliotrope.domain.entities.tag import Tag


def test_raw_galleryinfo_creation():
    raw_galleryinfo = RawGalleryinfo(
        date=datetime(2023, 10, 1),
        galleryurl="http://example.com",
        id=1,
        japanese_title="Japanese Title",
        language_localname="english",
        language_url="http://example.com/language",
        language="english",
        title="Test Title",
        type="manga",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 10, 1),
        artists=[Artist(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            Character(character="Character Name", url="http://example.com/character")
        ],
        files=[
            File(
                hasavif=True,
                haswebp=False,
                hash="abcdef1234567890abcdef1234567890",
                name="file1.jpg",
                width=800,
                height=600,
                hasjxl=False,
                single=True,
            )
        ],
        groups=[Group(group="Group Name", url="http://example.com/group")],
        languages=[
            RawLanguage(
                galleryid=1,
                language_localname="english",
                name="English",
                url="http://example.com/language",
            )
        ],
        parodys=[Parody(parody="Parody Name", url="http://example.com/parody")],
        related=[2, 3, 4],
        scene_indexes=[1, 2, 3],
        tags=[
            Tag(
                tag="Tag Name",
                url="http://example.com/tag",
                male=False,
                female=False,
            )
        ],
    )

    assert raw_galleryinfo.date == datetime(2023, 10, 1)
    assert raw_galleryinfo.galleryurl == "http://example.com"
    assert raw_galleryinfo.id == 1
    assert raw_galleryinfo.japanese_title == "Japanese Title"
    assert raw_galleryinfo.language_localname == "english"
    assert raw_galleryinfo.language_url == "http://example.com/language"
    assert raw_galleryinfo.language == "english"
    assert raw_galleryinfo.title == "Test Title"
    assert raw_galleryinfo.type == "manga"
    assert raw_galleryinfo.video is None
    assert raw_galleryinfo.videofilename is None
    assert raw_galleryinfo.blocked is False
    assert raw_galleryinfo.datepublished == date(2023, 10, 1)
    assert len(raw_galleryinfo.artists) == 1
    assert raw_galleryinfo.artists[0].artist == "Artist Name"
    assert len(raw_galleryinfo.characters) == 1
    assert raw_galleryinfo.characters[0].character == "Character Name"
    assert len(raw_galleryinfo.files) == 1
    assert raw_galleryinfo.files[0].name == "file1.jpg"
    assert len(raw_galleryinfo.groups) == 1
    assert raw_galleryinfo.groups[0].group == "Group Name"
    assert len(raw_galleryinfo.languages) == 1
    assert raw_galleryinfo.languages[0].name == "English"
    assert len(raw_galleryinfo.parodys) == 1
    assert raw_galleryinfo.parodys[0].parody == "Parody Name"
    assert raw_galleryinfo.related == [2, 3, 4]
    assert raw_galleryinfo.scene_indexes == [1, 2, 3]
    assert len(raw_galleryinfo.tags) == 1
    assert raw_galleryinfo.tags[0].tag == "Tag Name"


def test_raw_galleryinfo_serialization():
    raw_galleryinfo = RawGalleryinfo(
        date=datetime(2023, 10, 1),
        galleryurl="http://example.com",
        id=1,
        japanese_title="Japanese Title",
        language_localname="english",
        language_url="http://example.com/language",
        language="english",
        title="Test Title",
        type="manga",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 10, 1),
        artists=[Artist(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            Character(character="Character Name", url="http://example.com/character")
        ],
        files=[
            File(
                hasavif=True,
                haswebp=False,
                hash="abcdef1234567890abcdef1234567890",
                name="file1.jpg",
                width=800,
                height=600,
                hasjxl=False,
                single=True,
            )
        ],
        groups=[Group(group="Group Name", url="http://example.com/group")],
        languages=[
            RawLanguage(
                galleryid=1,
                language_localname="english",
                name="English",
                url="http://example.com/language",
            )
        ],
        parodys=[Parody(parody="Parody Name", url="http://example.com/parody")],
        related=[2, 3, 4],
        scene_indexes=[1, 2, 3],
        tags=[
            Tag(
                tag="Tag Name",
                url="http://example.com/tag",
                male=False,
                female=False,
            )
        ],
    )
    assert raw_galleryinfo.to_dict() == {
        "date": "2023-10-01T00:00:00",
        "galleryurl": "http://example.com",
        "id": 1,
        "japanese_title": "Japanese Title",
        "language_localname": "english",
        "language_url": "http://example.com/language",
        "language": "english",
        "title": "Test Title",
        "type": "manga",
        "video": None,
        "videofilename": None,
        "blocked": False,
        "datepublished": "2023-10-01",
        "artists": [{"artist": "Artist Name", "url": "http://example.com/artist"}],
        "characters": [
            {"character": "Character Name", "url": "http://example.com/character"}
        ],
        "files": [
            {
                "hasavif": True,
                "haswebp": False,
                "hash": "abcdef1234567890abcdef1234567890",
                "name": "file1.jpg",
                "width": 800,
                "height": 600,
                "hasjxl": False,
                "single": True,
            }
        ],
        "groups": [{"group": "Group Name", "url": "http://example.com/group"}],
        "languages": [
            {
                "galleryid": 1,
                "language_localname": "english",
                "name": "English",
                "url": "http://example.com/language",
            }
        ],
        "parodys": [{"parody": "Parody Name", "url": "http://example.com/parody"}],
        "related": [2, 3, 4],
        "scene_indexes": [1, 2, 3],
        "tags": [
            {
                "tag": "Tag Name",
                "url": "http://example.com/tag",
                "male": False,
                "female": False,
            }
        ],
    }


def test_raw_galleryinfo_deserialization():
    raw_galleryinfo = RawGalleryinfo.from_dict(
        {
            "date": "2023-10-01T00:00:00",
            "galleryurl": "http://example.com",
            "id": 1,
            "japanese_title": "Japanese Title",
            "language_localname": "english",
            "language_url": "http://example.com/language",
            "language": "english",
            "title": "Test Title",
            "type": "manga",
            "video": None,
            "videofilename": None,
            "blocked": False,
            "datepublished": "2023-10-01",
            "artists": [{"artist": "Artist Name", "url": "http://example.com/artist"}],
            "characters": [
                {"character": "Character Name", "url": "http://example.com/character"}
            ],
            "files": [
                {
                    "hasavif": True,
                    "haswebp": False,
                    "hash": "abcdef1234567890abcdef1234567890",
                    "name": "file1.jpg",
                    "width": 800,
                    "height": 600,
                    "hasjxl": False,
                    "single": True,
                }
            ],
            "groups": [{"group": "Group Name", "url": "http://example.com/group"}],
            "languages": [
                {
                    "galleryid": 1,
                    "language_localname": "english",
                    "name": "English",
                    "url": "http://example.com/language",
                }
            ],
            "parodys": [{"parody": "Parody Name", "url": "http://example.com/parody"}],
            "related": [2, 3, 4],
            "scene_indexes": [1, 2, 3],
            "tags": [
                {
                    "tag": "Tag Name",
                    "url": "http://example.com/tag",
                    "male": False,
                    "female": False,
                }
            ],
        }
    )
    assert raw_galleryinfo.date == datetime(2023, 10, 1)
    assert raw_galleryinfo.galleryurl == "http://example.com"
    assert raw_galleryinfo.id == 1
    assert raw_galleryinfo.japanese_title == "Japanese Title"
    assert raw_galleryinfo.language_localname == "english"
    assert raw_galleryinfo.language_url == "http://example.com/language"
    assert raw_galleryinfo.language == "english"
    assert raw_galleryinfo.title == "Test Title"
    assert raw_galleryinfo.type == "manga"
    assert raw_galleryinfo.video is None
    assert raw_galleryinfo.videofilename is None
    assert raw_galleryinfo.blocked is False
    assert raw_galleryinfo.datepublished == date(2023, 10, 1)
    assert len(raw_galleryinfo.artists) == 1
    assert raw_galleryinfo.artists[0].artist == "Artist Name"
    assert len(raw_galleryinfo.characters) == 1
    assert raw_galleryinfo.characters[0].character == "Character Name"
    assert len(raw_galleryinfo.files) == 1
    assert raw_galleryinfo.files[0].name == "file1.jpg"
    assert len(raw_galleryinfo.groups) == 1
    assert raw_galleryinfo.groups[0].group == "Group Name"
    assert len(raw_galleryinfo.languages) == 1
    assert raw_galleryinfo.languages[0].name == "English"
    assert len(raw_galleryinfo.parodys) == 1
    assert raw_galleryinfo.parodys[0].parody == "Parody Name"
    assert raw_galleryinfo.related == [2, 3, 4]
    assert raw_galleryinfo.scene_indexes == [1, 2, 3]
    assert len(raw_galleryinfo.tags) == 1
    assert raw_galleryinfo.tags[0].tag == "Tag Name"


def test_raw_galleryinfo_equality():
    raw_galleryinfo1 = RawGalleryinfo(
        date=datetime(2023, 10, 1),
        galleryurl="http://example.com",
        id=1,
        japanese_title="Japanese Title",
        language_localname="english",
        language_url="http://example.com/language",
        language="english",
        title="Test Title",
        type="manga",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 10, 1),
        artists=[Artist(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            Character(character="Character Name", url="http://example.com/character")
        ],
        files=[
            File(
                hasavif=True,
                haswebp=False,
                hash="abcdef1234567890abcdef1234567890",
                name="file1.jpg",
                width=800,
                height=600,
                hasjxl=False,
                single=True,
            )
        ],
        groups=[Group(group="Group Name", url="http://example.com/group")],
        languages=[
            RawLanguage(
                galleryid=1,
                language_localname="english",
                name="English",
                url="http://example.com/language",
            )
        ],
        parodys=[Parody(parody="Parody Name", url="http://example.com/parody")],
        related=[2, 3, 4],
        scene_indexes=[1, 2, 3],
        tags=[
            Tag(
                tag="Tag Name",
                url="http://example.com/tag",
                male=False,
                female=False,
            )
        ],
    )

    raw_galleryinfo2 = RawGalleryinfo(
        date=datetime(2023, 10, 1),
        galleryurl="http://example.com",
        id=1,
        japanese_title="Japanese Title",
        language_localname="english",
        language_url="http://example.com/language",
        language="english",
        title="Test Title",
        type="manga",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 10, 1),
        artists=[Artist(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            Character(character="Character Name", url="http://example.com/character")
        ],
        files=[
            File(
                hasavif=True,
                haswebp=False,
                hash="abcdef1234567890abcdef1234567890",
                name="file1.jpg",
                width=800,
                height=600,
                hasjxl=False,
                single=True,
            )
        ],
        groups=[Group(group="Group Name", url="http://example.com/group")],
        languages=[
            RawLanguage(
                galleryid=1,
                language_localname="english",
                name="English",
                url="http://example.com/language",
            )
        ],
        parodys=[Parody(parody="Parody Name", url="http://example.com/parody")],
        related=[2, 3, 4],
        scene_indexes=[1, 2, 3],
        tags=[
            Tag(
                tag="Tag Name",
                url="http://example.com/tag",
                male=False,
                female=False,
            )
        ],
    )

    raw_galleryinfo3 = RawGalleryinfo(
        date=datetime(2023, 11, 1),
        galleryurl="http://example.org",
        id=2,
        japanese_title="Different Title",
        language_localname="japanese",
        language_url="http://example.org/language",
        language="japanese",
        title="Different Title",
        type="doujinshi",
        video=None,
        videofilename=None,
        blocked=True,
        datepublished=date(2023, 11, 1),
        artists=[Artist(artist="Different Artist", url="http://example.org/artist")],
        characters=[
            Character(
                character="Different Character", url="http://example.org/character"
            )
        ],
        files=[
            File(
                hasavif=False,
                haswebp=True,
                hash="1234567890abcdef1234567890abcdef",
                name="file2.png",
                width=1024,
                height=768,
                hasjxl=True,
                single=False,
            )
        ],
        groups=[Group(group="Different Group", url="http://example.org/group")],
        languages=[
            RawLanguage(
                galleryid=2,
                language_localname="japanese",
                name="Japanese",
                url="http://example.org/language",
            )
        ],
        parodys=[Parody(parody="Different Parody", url="http://example.org/parody")],
        related=[5, 6, 7],
        scene_indexes=[4, 5, 6],
        tags=[
            Tag(
                tag="Different Tag",
                url="http://example.org/tag",
                male=False,
                female=False,
            )
        ],
    )
    assert raw_galleryinfo1 == raw_galleryinfo2
    assert raw_galleryinfo1 != raw_galleryinfo3
