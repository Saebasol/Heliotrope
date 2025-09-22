from datetime import date, datetime

import pytest

from heliotrope.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from heliotrope.infrastructure.sqlalchemy.entities.character import CharacterSchema
from heliotrope.infrastructure.sqlalchemy.entities.file import FileSchema
from heliotrope.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from heliotrope.infrastructure.sqlalchemy.entities.group import GroupSchema
from heliotrope.infrastructure.sqlalchemy.entities.language import LanguageSchema
from heliotrope.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from heliotrope.infrastructure.sqlalchemy.entities.parody import ParodySchema
from heliotrope.infrastructure.sqlalchemy.entities.related import RelatedSchema
from heliotrope.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from heliotrope.infrastructure.sqlalchemy.entities.tag import TagSchema
from heliotrope.infrastructure.sqlalchemy.entities.type import TypeSchema


@pytest.fixture()
def sample_artist_schema():
    return ArtistSchema(artist="Artist Name", url="http://example.com/artist")


@pytest.fixture()
def sample_character_schema():
    return CharacterSchema(
        character="Character Name", url="http://example.com/character"
    )


@pytest.fixture()
def sample_file_schema():
    return FileSchema(
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
def sample_group_schema():
    return GroupSchema(group="Group Name", url="http://example.com/group")


@pytest.fixture()
def sample_parody_schema():
    return ParodySchema(parody="Parody Name", url="http://example.com/parody")


@pytest.fixture()
def sample_tag_schema():
    return TagSchema(tag="Tag Name", url="http://example.com/tag")


@pytest.fixture()
def sample_tag_schema_female():
    return TagSchema(tag="Female Tag", url="http://example.com/tag/female", female=True)


@pytest.fixture()
def sample_tag_schema_male():
    return TagSchema(tag="Male Tag", url="http://example.com/tag/male", male=True)


@pytest.fixture()
def sample_language_info_schema():
    return LanguageInfoSchema(
        language="English", language_url="http://example.com/language"
    )


@pytest.fixture()
def sample_language_localname_schema():
    return LanguageLocalnameSchema(name="English")


@pytest.fixture()
def sample_language_schema():
    return LanguageSchema(
        language_info_id=1,
        localname_id=1,
        galleryid=12345,
        url="http://example.com/gallery",
        language_info=LanguageInfoSchema(
            id=1, language="English", language_url="http://example.com/language"
        ),
        language_localname=LanguageLocalnameSchema(id=1, name="English"),
    )


@pytest.fixture()
def sample_type_schema():
    return TypeSchema(type="Manga")


@pytest.fixture()
def sample_related_schema():
    return RelatedSchema(related_id=54321)


@pytest.fixture()
def sample_scene_index_schema():
    return SceneIndexSchema(scene_index=5)


@pytest.fixture()
def sample_galleryinfo_schema():
    return GalleryinfoSchema(
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
    )


@pytest.fixture()
def sample_galleryinfo_schema_with_relations(
    sample_artist_schema: ArtistSchema,
    sample_character_schema: CharacterSchema,
    sample_file_schema: FileSchema,
    sample_group_schema: GroupSchema,
    sample_parody_schema: ParodySchema,
    sample_tag_schema: TagSchema,
    sample_language_schema: LanguageSchema,
    sample_type_schema: TypeSchema,
    sample_language_info_schema: LanguageInfoSchema,
    sample_language_localname_schema: LanguageLocalnameSchema,
    sample_related_schema: RelatedSchema,
    sample_scene_index_schema: SceneIndexSchema,
):
    galleryinfo = GalleryinfoSchema(
        id=1,
        date=datetime(2023, 10, 1, 12, 0, 0),
        title="Complete Sample Title",
        japanese_title="完全なサンプルタイトル",
        galleryurl="http://example.com/gallery/complete",
        video="sample_video.mp4",
        videofilename="sample_video_filename.mp4",
        type_id=1,
        language_info_id=1,
        localname_id=1,
        datepublished=date(2023, 10, 1),
        blocked=False,
    )

    # Populate relationships
    galleryinfo.artists = [sample_artist_schema]
    galleryinfo.characters = [sample_character_schema]
    galleryinfo.files = [sample_file_schema]
    galleryinfo.groups = [sample_group_schema]
    galleryinfo.parodys = [sample_parody_schema]
    galleryinfo.tags = [sample_tag_schema]
    galleryinfo.languages = [sample_language_schema]
    galleryinfo.related = [sample_related_schema]
    galleryinfo.scene_indexes = [sample_scene_index_schema]
    galleryinfo.type = sample_type_schema
    galleryinfo.language_info = sample_language_info_schema
    galleryinfo.language_localname = sample_language_localname_schema

    return galleryinfo
