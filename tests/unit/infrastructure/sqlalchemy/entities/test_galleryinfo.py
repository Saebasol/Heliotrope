from datetime import date, datetime

from yggdrasil.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from yggdrasil.infrastructure.sqlalchemy.entities.character import CharacterSchema
from yggdrasil.infrastructure.sqlalchemy.entities.file import FileSchema
from yggdrasil.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from yggdrasil.infrastructure.sqlalchemy.entities.group import GroupSchema
from yggdrasil.infrastructure.sqlalchemy.entities.language import LanguageSchema
from yggdrasil.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from yggdrasil.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from yggdrasil.infrastructure.sqlalchemy.entities.parody import ParodySchema
from yggdrasil.infrastructure.sqlalchemy.entities.related import RelatedSchema
from yggdrasil.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from yggdrasil.infrastructure.sqlalchemy.entities.tag import TagSchema
from yggdrasil.infrastructure.sqlalchemy.entities.type import TypeSchema


def test_galleryinfo_schema_creation():
    galleryinfo = GalleryinfoSchema(
        date=datetime(2023, 10, 1, 12, 0, 0),
        title="Sample Title",
        japanese_title="サンプルタイトル",
        galleryurl="http://example.com/gallery",
        video=None,
        videofilename=None,
        type_id=1,
        language_info_id=1,
        localname_id=1,
        datepublished=date(2023, 10, 1),
        blocked=False,
        artists=[ArtistSchema(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            CharacterSchema(
                character="Character Name", url="http://example.com/character"
            )
        ],
        files=[
            FileSchema(
                name="file1.jpg",
                hasavif=False,
                haswebp=False,
                width=800,
                height=600,
                hash="abcdef1234567890abcdef1234567890",
            )
        ],
        groups=[GroupSchema(group="Group Name", url="http://example.com/group")],
        parodys=[ParodySchema(parody="Parody Name", url="http://example.com/parody")],
        tags=[TagSchema(tag="Tag Name", url="http://example.com/tag")],
        languages=[
            LanguageSchema(
                galleryid=12345,
                url="http://example.com/language",
                language_info_id=1,
                localname_id=1,
                language_info=LanguageInfoSchema(
                    id=1, language="English", language_url="http://example.com/language"
                ),
                language_localname=LanguageLocalnameSchema(id=1, name="English"),
            )
        ],
        related=[RelatedSchema(related_id=54321)],
        scene_indexes=[SceneIndexSchema(scene_index=5)],
        type=TypeSchema(type="Manga"),
        language_info=LanguageInfoSchema(
            language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(name="English"),
    )

    assert galleryinfo.date == datetime(2023, 10, 1, 12, 0, 0)
    assert galleryinfo.title == "Sample Title"
    assert galleryinfo.japanese_title == "サンプルタイトル"
    assert galleryinfo.galleryurl == "http://example.com/gallery"
    assert galleryinfo.video is None
    assert galleryinfo.videofilename is None
    assert galleryinfo.type_id == 1
    assert galleryinfo.language_info_id == 1
    assert galleryinfo.localname_id == 1
    assert galleryinfo.datepublished == date(2023, 10, 1)
    assert galleryinfo.blocked is False
    assert len(galleryinfo.artists) == 1
    assert len(galleryinfo.characters) == 1
    assert len(galleryinfo.files) == 1
    assert len(galleryinfo.groups) == 1
    assert len(galleryinfo.parodys) == 1
    assert len(galleryinfo.tags) == 1
    assert len(galleryinfo.languages) == 1
    assert len(galleryinfo.related) == 1
    assert len(galleryinfo.scene_indexes) == 1


def test_galleryinfo_schema_serialization():
    galleryinfo = GalleryinfoSchema(
        date=datetime(2023, 10, 1, 12, 0, 0),
        title="Sample Title",
        japanese_title="サンプルタイトル",
        galleryurl="http://example.com/gallery",
        video=None,
        videofilename=None,
        type_id=1,
        language_info_id=1,
        localname_id=1,
        datepublished=date(2023, 10, 1),
        blocked=False,
        artists=[ArtistSchema(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            CharacterSchema(
                character="Character Name", url="http://example.com/character"
            )
        ],
        files=[
            FileSchema(
                name="file1.jpg",
                hasavif=False,
                haswebp=False,
                width=800,
                height=600,
                hash="abcdef1234567890abcdef1234567890",
            )
        ],
        groups=[GroupSchema(group="Group Name", url="http://example.com/group")],
        parodys=[ParodySchema(parody="Parody Name", url="http://example.com/parody")],
        tags=[TagSchema(tag="Tag Name", url="http://example.com/tag")],
        languages=[
            LanguageSchema(
                galleryid=12345,
                url="http://example.com/language",
                language_info_id=1,
                localname_id=1,
                language_info=LanguageInfoSchema(
                    id=1, language="English", language_url="http://example.com/language"
                ),
                language_localname=LanguageLocalnameSchema(id=1, name="English"),
            )
        ],
        related=[RelatedSchema(related_id=54321)],
        scene_indexes=[SceneIndexSchema(scene_index=5)],
        type=TypeSchema(type="Manga"),
        language_info=LanguageInfoSchema(
            language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(name="English"),
    )
    serialized = galleryinfo.to_dict()

    assert "date" in serialized
    assert "title" in serialized
    assert "galleryurl" in serialized
    assert "blocked" in serialized
    assert serialized["title"] == "Sample Title"
    assert serialized["galleryurl"] == "http://example.com/gallery"
    assert serialized["blocked"] is False
    assert serialized["date"] == "2023-10-01T12:00:00"
    assert serialized["languages"][0]["galleryid"] == 12345


def test_galleryinfo_schema_deserialization():
    data = {
        "id": 1,
        "type_id": 1,
        "language_info_id": 1,
        "localname_id": 1,
        "date": "2023-10-01T12:00:00",
        "title": "Sample Title",
        "japanese_title": "サンプルタイトル",
        "galleryurl": "http://example.com/gallery",
        "video": None,
        "videofilename": None,
        "datepublished": "2023-10-01",
        "blocked": False,
        "artists": [{"artist": "Artist Name", "url": "http://example.com/artist"}],
        "characters": [
            {"character": "Character Name", "url": "http://example.com/character"}
        ],
        "groups": [{"group": "Group Name", "url": "http://example.com/group"}],
        "parodys": [{"parody": "Parody Name", "url": "http://example.com/parody"}],
        "tags": [
            {
                "tag": "Tag Name",
                "url": "http://example.com/tag",
                "female": False,
                "male": False,
            }
        ],
        "related": [54321],
        "scene_indexes": [5],
        "files": [
            {
                "hasavif": False,
                "hash": "abcdef1234567890abcdef1234567890",
                "height": 600,
                "name": "file1.jpg",
                "width": 800,
                "hasjxl": False,
                "haswebp": False,
                "single": False,
            }
        ],
        "languages": [
            {
                "galleryid": 12345,
                "url": "http://example.com/language",
                "language_info": {
                    "language": "English",
                    "language_url": "http://example.com/language",
                },
                "language_localname": {"name": "English"},
                "language_info_id": 1,
                "localname_id": 1,
            }
        ],
        "type": {"type": "Manga"},
        "language_info": {
            "language": "English",
            "language_url": "http://example.com/language",
        },
        "language_localname": {"name": "English"},
    }
    galleryinfo = GalleryinfoSchema.from_dict(data)

    assert galleryinfo.date == datetime(2023, 10, 1, 12, 0, 0)
    assert galleryinfo.title == "Sample Title"
    assert galleryinfo.galleryurl == "http://example.com/gallery"
    assert galleryinfo.blocked is False


def test_galleryinfo_schema_equality():
    galleryinfo1 = GalleryinfoSchema(
        id=1,
        date=datetime(2023, 10, 1, 12, 0, 0),
        title="Sample Title",
        japanese_title="サンプルタイトル",
        galleryurl="http://example.com/gallery",
        video=None,
        videofilename=None,
        type_id=1,
        language_info_id=1,
        localname_id=1,
        datepublished=date(2023, 10, 1),
        blocked=False,
        artists=[ArtistSchema(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            CharacterSchema(
                character="Character Name", url="http://example.com/character"
            )
        ],
        files=[
            FileSchema(
                name="file1.jpg",
                hasavif=False,
                haswebp=False,
                width=800,
                height=600,
                hash="abcdef1234567890abcdef1234567890",
            )
        ],
        groups=[GroupSchema(group="Group Name", url="http://example.com/group")],
        parodys=[ParodySchema(parody="Parody Name", url="http://example.com/parody")],
        tags=[TagSchema(tag="Tag Name", url="http://example.com/tag")],
        languages=[
            LanguageSchema(
                galleryid=12345,
                url="http://example.com/language",
                language_info_id=1,
                localname_id=1,
                language_info=LanguageInfoSchema(
                    id=1, language="English", language_url="http://example.com/language"
                ),
                language_localname=LanguageLocalnameSchema(id=1, name="English"),
            )
        ],
        related=[RelatedSchema(related_id=54321)],
        scene_indexes=[SceneIndexSchema(scene_index=5)],
        type=TypeSchema(type="Manga"),
        language_info=LanguageInfoSchema(
            language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(name="English"),
    )
    galleryinfo2 = GalleryinfoSchema(
        id=1,
        date=datetime(2023, 10, 1, 12, 0, 0),
        title="Sample Title",
        japanese_title="サンプルタイトル",
        galleryurl="http://example.com/gallery",
        video=None,
        videofilename=None,
        type_id=1,
        language_info_id=1,
        localname_id=1,
        datepublished=date(2023, 10, 1),
        blocked=False,
        artists=[ArtistSchema(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            CharacterSchema(
                character="Character Name", url="http://example.com/character"
            )
        ],
        files=[
            FileSchema(
                name="file1.jpg",
                hasavif=False,
                haswebp=False,
                width=800,
                height=600,
                hash="abcdef1234567890abcdef1234567890",
            )
        ],
        groups=[GroupSchema(group="Group Name", url="http://example.com/group")],
        parodys=[ParodySchema(parody="Parody Name", url="http://example.com/parody")],
        tags=[TagSchema(tag="Tag Name", url="http://example.com/tag")],
        languages=[
            LanguageSchema(
                galleryid=12345,
                url="http://example.com/language",
                language_info_id=1,
                localname_id=1,
                language_info=LanguageInfoSchema(
                    id=1, language="English", language_url="http://example.com/language"
                ),
                language_localname=LanguageLocalnameSchema(id=1, name="English"),
            )
        ],
        related=[RelatedSchema(related_id=54321)],
        scene_indexes=[SceneIndexSchema(scene_index=5)],
        type=TypeSchema(type="Manga"),
        language_info=LanguageInfoSchema(
            language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(name="English"),
    )
    galleryinfo3 = GalleryinfoSchema(
        id=2,
        date=datetime(2023, 10, 1, 12, 0, 0),
        title="Sample Title",
        japanese_title="サンプルタイトル",
        galleryurl="http://example.com/gallery",
        video=None,
        videofilename=None,
        type_id=1,
        language_info_id=1,
        localname_id=1,
        datepublished=date(2023, 10, 1),
        blocked=False,
        artists=[ArtistSchema(artist="Artist Name", url="http://example.com/artist")],
        characters=[
            CharacterSchema(
                character="Character Name", url="http://example.com/character"
            )
        ],
        files=[
            FileSchema(
                name="file1.jpg",
                hasavif=False,
                haswebp=False,
                width=800,
                height=600,
                hash="abcdef1234567890abcdef1234567890",
            )
        ],
        groups=[GroupSchema(group="Group Name", url="http://example.com/group")],
        parodys=[ParodySchema(parody="Parody Name", url="http://example.com/parody")],
        tags=[TagSchema(tag="Tag Name", url="http://example.com/tag")],
        languages=[
            LanguageSchema(
                galleryid=12345,
                url="http://example.com/language",
                language_info_id=1,
                localname_id=1,
                language_info=LanguageInfoSchema(
                    id=1, language="English", language_url="http://example.com/language"
                ),
                language_localname=LanguageLocalnameSchema(id=1, name="English"),
            )
        ],
        related=[RelatedSchema(related_id=54321)],
        scene_indexes=[SceneIndexSchema(scene_index=5)],
        type=TypeSchema(type="Manga"),
        language_info=LanguageInfoSchema(
            language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(name="English"),
    )

    assert galleryinfo1 == galleryinfo2
    assert galleryinfo1 != galleryinfo3
