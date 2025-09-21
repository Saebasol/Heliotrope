from datetime import date, datetime

import pytest

from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.entities.character import Character
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.group import Group
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.entities.language_localname import LanguageLocalname
from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.entities.raw_galleryinfo import RawGalleryinfo
from heliotrope.domain.entities.raw_language import RawLanguage
from heliotrope.domain.entities.tag import Tag
from heliotrope.domain.entities.type import Type


@pytest.fixture()
def sample_artist():
    return Artist(artist="Artist Name", url="http://example.com/artist")


@pytest.fixture()
def sample_character():
    return Character(character="Character Name", url="http://example.com/character")


@pytest.fixture()
def sample_file():
    return File(
        hasavif=True,
        haswebp=False,
        hash="abcdef1234567890abcdef1234567890",
        name="file1.jpg",
        width=800,
        height=600,
        hasjxl=False,
        single=True,
    )


@pytest.fixture()
def sample_group():
    return Group(group="Group Name", url="http://example.com/group")


@pytest.fixture()
def sample_parody():
    return Parody(parody="Parody Name", url="http://example.com/parody")


@pytest.fixture()
def sample_tag():
    return Tag(tag="Tag Name", url="http://example.com/tag")


@pytest.fixture()
def sample_language_info():
    return LanguageInfo(language="English", language_url="http://example.com/language")


@pytest.fixture()
def sample_language_localname():
    return LanguageLocalname(name="English")


@pytest.fixture()
def sample_language(
    sample_language_info: LanguageInfo,
    sample_language_localname: LanguageLocalname,
):
    return Language(
        galleryid=1,
        url="http://example.com/gallery",
        language_localname=sample_language_localname,
        language_info=sample_language_info,
    )


@pytest.fixture()
def sample_type():
    return Type(type="Manga")


@pytest.fixture()
def sample_raw_language():
    return RawLanguage(
        galleryid=1,
        language_localname="English",
        name="English",
        url="http://example.com/language",
    )


@pytest.fixture()
def sample_raw_galleryinfo(
    sample_artist: Artist,
    sample_character: Character,
    sample_file: File,
    sample_group: Group,
    sample_parody: Parody,
    sample_tag: Tag,
    sample_raw_language: RawLanguage,
):
    return RawGalleryinfo(
        date=datetime(2023, 10, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery",
        id=12345,
        japanese_title="サンプルタイトル",
        language_localname="English",
        language_url="http://example.com/language",
        language="English",
        title="Sample Title",
        type="Manga",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 10, 1),
        artists=[sample_artist],
        characters=[sample_character],
        files=[sample_file],
        groups=[sample_group],
        languages=[sample_raw_language],
        parodys=[sample_parody],
        related=[54321, 67890],
        scene_indexes=[1, 2, 3],
        tags=[sample_tag],
    )


@pytest.fixture()
def sample_galleryinfo(
    sample_artist: Artist,
    sample_character: Character,
    sample_file: File,
    sample_group: Group,
    sample_parody: Parody,
    sample_tag: Tag,
    sample_language: Language,
    sample_language_info: LanguageInfo,
    sample_language_localname: LanguageLocalname,
    sample_type: Type,
):
    return Galleryinfo(
        date=datetime(2023, 10, 1, 12, 0, 0),
        galleryurl="http://example.com/gallery",
        id=12345,
        language_info=sample_language_info,
        language_localname=sample_language_localname,
        japanese_title="サンプルタイトル",
        title="Sample Title",
        type=sample_type,
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 10, 1),
        artists=[sample_artist],
        characters=[sample_character],
        files=[sample_file],
        groups=[sample_group],
        languages=[sample_language],
        parodys=[sample_parody],
        related=[54321, 67890],
        scene_indexes=[1, 2, 3],
        tags=[sample_tag],
    )
