from datetime import date, datetime

from yggdrasil.domain.entities.artist import Artist
from yggdrasil.domain.entities.character import Character
from yggdrasil.domain.entities.file import File
from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.domain.entities.group import Group
from yggdrasil.domain.entities.language import Language
from yggdrasil.domain.entities.language_info import LanguageInfo
from yggdrasil.domain.entities.language_localname import LanguageLocalname
from yggdrasil.domain.entities.parody import Parody
from yggdrasil.domain.entities.tag import Tag
from yggdrasil.domain.entities.type import Type


def test_galleryinfo_creation():
    language_info = LanguageInfo(language="english", language_url="https://example.com")
    language_localname = LanguageLocalname(name="english")
    language = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    galleryinfo = Galleryinfo(
        date=datetime(2023, 1, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery/1",
        id=1,
        japanese_title="テストギャラリー",
        language_localname=language_localname,
        language_info=language_info,
        title="Test Gallery",
        type=Type(type="doujinshi"),
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 1, 1),
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
        languages=[language],
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

    assert galleryinfo.date == datetime(2023, 1, 1, 12, 0, 0)
    assert galleryinfo.galleryurl == "http://example.com/gallery/1"
    assert galleryinfo.id == 1
    assert galleryinfo.japanese_title == "テストギャラリー"
    assert isinstance(galleryinfo.language_localname, LanguageLocalname)
    assert isinstance(galleryinfo.language_info, LanguageInfo)
    assert galleryinfo.title == "Test Gallery"
    assert galleryinfo.type.type == "doujinshi"
    assert galleryinfo.video is None
    assert galleryinfo.videofilename is None
    assert galleryinfo.blocked is False
    assert galleryinfo.datepublished == date(2023, 1, 1)
    assert len(galleryinfo.artists) == 1
    assert len(galleryinfo.characters) == 1
    assert len(galleryinfo.files) == 1
    assert len(galleryinfo.groups) == 1
    assert len(galleryinfo.languages) == 1
    assert len(galleryinfo.parodys) == 1
    assert galleryinfo.related == [2, 3, 4]
    assert galleryinfo.scene_indexes == [1, 2, 3]
    assert len(galleryinfo.tags) == 1


def test_galleryinfo_serialization():
    language_info = LanguageInfo(language="english", language_url="https://example.com")
    language_localname = LanguageLocalname(name="english")
    language = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    galleryinfo = Galleryinfo(
        date=datetime(2023, 1, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery/1",
        id=1,
        japanese_title="テストギャラリー",
        language_localname=language_localname,
        language_info=language_info,
        title="Test Gallery",
        type=Type(type="doujinshi"),
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 1, 1),
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
        languages=[language],
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

    assert galleryinfo.to_dict() == {
        "date": "2023-01-01T12:00:00",
        "galleryurl": "http://example.com/gallery/1",
        "id": 1,
        "japanese_title": "テストギャラリー",
        "language_info": {"language": "english", "language_url": "https://example.com"},
        "language_localname": {"name": "english"},
        "title": "Test Gallery",
        "type": {"type": "doujinshi"},
        "video": None,
        "videofilename": None,
        "blocked": False,
        "datepublished": "2023-01-01",
        "artists": [{"artist": "Artist Name", "url": "http://example.com/artist"}],
        "characters": [
            {"character": "Character Name", "url": "http://example.com/character"}
        ],
        "files": [
            {
                "hasavif": True,
                "hash": "abcdef1234567890abcdef1234567890",
                "height": 600,
                "name": "file1.jpg",
                "width": 800,
                "hasjxl": False,
                "haswebp": False,
                "single": True,
            }
        ],
        "groups": [{"group": "Group Name", "url": "http://example.com/group"}],
        "languages": [
            {
                "galleryid": 1,
                "url": "http://example.com",
                "language_localname": {"name": "english"},
                "language_info": {
                    "language": "english",
                    "language_url": "https://example.com",
                },
            }
        ],
        "parodys": [{"parody": "Parody Name", "url": "http://example.com/parody"}],
        "related": [2, 3, 4],
        "scene_indexes": [1, 2, 3],
        "tags": [
            {
                "tag": "Tag Name",
                "url": "http://example.com/tag",
                "female": False,
                "male": False,
            }
        ],
    }


def test_galleryinfo_deserialization():
    galleryinfo = Galleryinfo.from_dict(
        {
            "date": "2023-01-01T12:00:00",
            "galleryurl": "http://example.com/gallery/1",
            "id": 1,
            "japanese_title": "テストギャラリー",
            "language_info": {
                "language": "english",
                "language_url": "https://example.com",
            },
            "language_localname": {"name": "english"},
            "title": "Test Gallery",
            "type": {"type": "doujinshi"},
            "video": None,
            "videofilename": None,
            "blocked": False,
            "datepublished": "2023-01-01",
            "artists": [{"artist": "Artist Name", "url": "http://example.com/artist"}],
            "characters": [
                {"character": "Character Name", "url": "http://example.com/character"}
            ],
            "files": [
                {
                    "hasavif": True,
                    "hash": "abcdef1234567890abcdef1234567890",
                    "height": 600,
                    "name": "file1.jpg",
                    "width": 800,
                    "hasjxl": False,
                    "haswebp": False,
                    "single": True,
                }
            ],
            "groups": [{"group": "Group Name", "url": "http://example.com/group"}],
            "languages": [
                {
                    "galleryid": 1,
                    "url": "http://example.com",
                    "language_localname": {"name": "english"},
                    "language_info": {
                        "language": "english",
                        "language_url": "https://example.com",
                    },
                }
            ],
            "parodys": [{"parody": "Parody Name", "url": "http://example.com/parody"}],
            "related": [2, 3, 4],
            "scene_indexes": [1, 2, 3],
            "tags": [
                {
                    "tag": "Tag Name",
                    "url": "http://example.com/tag",
                    "female": False,
                    "male": False,
                }
            ],
        }
    )

    assert galleryinfo.date == datetime(2023, 1, 1, 12, 0, 0)
    assert galleryinfo.galleryurl == "http://example.com/gallery/1"
    assert galleryinfo.id == 1
    assert galleryinfo.japanese_title == "テストギャラリー"
    assert isinstance(galleryinfo.language_localname, LanguageLocalname)
    assert isinstance(galleryinfo.language_info, LanguageInfo)
    assert galleryinfo.title == "Test Gallery"
    assert galleryinfo.type.type == "doujinshi"
    assert galleryinfo.video is None
    assert galleryinfo.videofilename is None
    assert galleryinfo.blocked is False
    assert galleryinfo.datepublished == date(2023, 1, 1)
    assert len(galleryinfo.artists) == 1
    assert len(galleryinfo.characters) == 1
    assert len(galleryinfo.files) == 1
    assert len(galleryinfo.groups) == 1
    assert len(galleryinfo.languages) == 1
    assert len(galleryinfo.parodys) == 1
    assert galleryinfo.related == [2, 3, 4]
    assert galleryinfo.scene_indexes == [1, 2, 3]
    assert len(galleryinfo.tags) == 1


def test_galleryinfo_equality():
    language_info = LanguageInfo(language="english", language_url="https://example.com")
    language_localname = LanguageLocalname(name="english")
    language = Language(
        galleryid=1,
        url="http://example.com",
        language_localname=language_localname,
        language_info=language_info,
    )

    galleryinfo1 = Galleryinfo(
        date=datetime(2023, 1, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery/1",
        id=1,
        japanese_title="テストギャラリー",
        language_localname=language_localname,
        language_info=language_info,
        title="Test Gallery",
        type=Type(type="doujinshi"),
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 1, 1),
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
        languages=[language],
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

    galleryinfo2 = Galleryinfo(
        date=datetime(2023, 1, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery/1",
        id=1,
        japanese_title="テストギャラリー",
        language_localname=language_localname,
        language_info=language_info,
        title="Test Gallery",
        type=Type(type="doujinshi"),
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 1, 1),
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
        languages=[language],
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

    galleryinfo3 = Galleryinfo(
        date=datetime(2024, 1, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery/2",
        id=2,
        japanese_title="別のギャラリー",
        language_localname=LanguageLocalname(name="japanese"),
        language_info=LanguageInfo(
            language="japanese", language_url="https://example.jp"
        ),
        title="Different Gallery",
        type=Type(type="manga"),
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2024, 1, 1),
        artists=[Artist(artist="Different Artist", url="http://example.com/artist2")],
        characters=[
            Character(
                character="Different Character", url="http://example.com/character2"
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
        groups=[Group(group="Different Group", url="http://example.com/group2")],
        languages=[
            Language(
                galleryid=2,
                url="http://example.com/lang2",
                language_localname=LanguageLocalname(name="japanese"),
                language_info=LanguageInfo(
                    language="japanese", language_url="https://example.jp"
                ),
            )
        ],
        parodys=[Parody(parody="Different Parody", url="http://example.com/parody2")],
        related=[5, 6],
        scene_indexes=[4, 5],
        tags=[
            Tag(
                tag="Different Tag",
                url="http://example.com/tag2",
                male=False,
                female=False,
            )
        ],
    )

    assert galleryinfo1 == galleryinfo2
    assert galleryinfo1 != galleryinfo3
