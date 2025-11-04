from datetime import date, datetime

from yggdrasil.domain.entities.artist import Artist
from yggdrasil.domain.entities.character import Character
from yggdrasil.domain.entities.file import File
from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.domain.entities.group import Group
from yggdrasil.domain.entities.parody import Parody
from yggdrasil.domain.entities.raw_galleryinfo import RawGalleryinfo
from yggdrasil.domain.entities.raw_language import RawLanguage
from yggdrasil.domain.entities.tag import Tag


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


def test_raw_galleryinfo_from_galleryinfo(sample_galleryinfo: Galleryinfo):
    raw_galleryinfo = RawGalleryinfo.from_galleryinfo(sample_galleryinfo)

    assert raw_galleryinfo.date == sample_galleryinfo.date
    assert raw_galleryinfo.galleryurl == sample_galleryinfo.galleryurl
    assert raw_galleryinfo.id == sample_galleryinfo.id
    assert raw_galleryinfo.japanese_title == sample_galleryinfo.japanese_title
    assert (
        raw_galleryinfo.language_localname == sample_galleryinfo.language_localname.name
    )
    assert raw_galleryinfo.language_url == sample_galleryinfo.language_info.language_url
    assert raw_galleryinfo.language == sample_galleryinfo.language_info.language
    assert raw_galleryinfo.title == sample_galleryinfo.title
    assert raw_galleryinfo.type == sample_galleryinfo.type.type
    assert raw_galleryinfo.video == sample_galleryinfo.video
    assert raw_galleryinfo.videofilename == sample_galleryinfo.videofilename
    assert raw_galleryinfo.blocked == sample_galleryinfo.blocked
    assert raw_galleryinfo.datepublished == sample_galleryinfo.datepublished
    assert raw_galleryinfo.artists == sample_galleryinfo.artists
    assert raw_galleryinfo.characters == sample_galleryinfo.characters
    assert raw_galleryinfo.files == sample_galleryinfo.files
    assert raw_galleryinfo.groups == sample_galleryinfo.groups
    assert len(raw_galleryinfo.languages) == len(sample_galleryinfo.languages)
    for rl, l in zip(raw_galleryinfo.languages, sample_galleryinfo.languages):
        assert rl.galleryid == l.galleryid
        assert rl.language_localname == l.language_localname.name
        assert rl.name == l.language_info.language
        assert rl.url == l.url
    assert raw_galleryinfo.parodys == sample_galleryinfo.parodys
    assert raw_galleryinfo.related == sample_galleryinfo.related
    assert raw_galleryinfo.scene_indexes == sample_galleryinfo.scene_indexes
    assert raw_galleryinfo.tags == sample_galleryinfo.tags


def test_raw_galleryinfo_to_galleryinfo(sample_raw_galleryinfo: RawGalleryinfo):
    galleryinfo = sample_raw_galleryinfo.to_galleryinfo()

    assert galleryinfo.date == sample_raw_galleryinfo.date
    assert galleryinfo.galleryurl == sample_raw_galleryinfo.galleryurl
    assert galleryinfo.id == sample_raw_galleryinfo.id
    assert galleryinfo.japanese_title == sample_raw_galleryinfo.japanese_title
    assert (
        galleryinfo.language_localname.name == sample_raw_galleryinfo.language_localname
    )
    assert galleryinfo.language_info.language_url == sample_raw_galleryinfo.language_url
    assert galleryinfo.language_info.language == sample_raw_galleryinfo.language
    assert galleryinfo.title == sample_raw_galleryinfo.title
    assert galleryinfo.type.type == sample_raw_galleryinfo.type
    assert galleryinfo.video == sample_raw_galleryinfo.video
    assert galleryinfo.videofilename == sample_raw_galleryinfo.videofilename
    assert galleryinfo.blocked == sample_raw_galleryinfo.blocked
    assert galleryinfo.datepublished == sample_raw_galleryinfo.datepublished
    assert galleryinfo.artists == sample_raw_galleryinfo.artists
    assert galleryinfo.characters == sample_raw_galleryinfo.characters
    assert galleryinfo.files == sample_raw_galleryinfo.files
    assert galleryinfo.groups == sample_raw_galleryinfo.groups
    assert len(galleryinfo.languages) == len(sample_raw_galleryinfo.languages)
    for l, rl in zip(galleryinfo.languages, sample_raw_galleryinfo.languages):
        assert l.galleryid == rl.galleryid
        assert l.language_localname.name == rl.language_localname
        assert l.language_info.language == rl.name
        assert l.url == rl.url
    assert galleryinfo.parodys == sample_raw_galleryinfo.parodys
    assert galleryinfo.related == sample_raw_galleryinfo.related
    assert galleryinfo.scene_indexes == sample_raw_galleryinfo.scene_indexes
    assert galleryinfo.tags == sample_raw_galleryinfo.tags
