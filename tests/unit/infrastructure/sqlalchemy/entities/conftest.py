import pytest

from heliotrope.domain.entities.artist import Artist
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
from tests.unit.domain.entities.conftest import *


@pytest.fixture()
def sample_artist_schema(sample_artist: Artist):
    return ArtistSchema.from_dict(sample_artist.to_dict())


@pytest.fixture()
def sample_character_schema(sample_character: Character):
    return CharacterSchema.from_dict(sample_character.to_dict())


@pytest.fixture()
def sample_file_schema(sample_file: File):
    return FileSchema.from_dict(sample_file.to_dict())


@pytest.fixture()
def sample_group_schema(sample_group: Group):
    return GroupSchema.from_dict(sample_group.to_dict())


@pytest.fixture()
def sample_parody_schema(sample_parody: Parody):
    return ParodySchema.from_dict(sample_parody.to_dict())


@pytest.fixture()
def sample_tag_schema(sample_tag: Tag):
    return TagSchema.from_dict(sample_tag.to_dict())


@pytest.fixture()
def sample_tag_schema_female(sample_tag_female: Tag):
    return TagSchema.from_dict(sample_tag_female.to_dict())


@pytest.fixture()
def sample_tag_schema_male(sample_tag_male: Tag):
    return TagSchema.from_dict(sample_tag_male.to_dict())


@pytest.fixture()
def sample_language_info_schema(sample_language_info: LanguageInfo):
    return LanguageInfoSchema.from_dict(sample_language_info.to_dict())


@pytest.fixture()
def sample_language_localname_schema(sample_language_localname: LanguageLocalname):
    return LanguageLocalnameSchema.from_dict(sample_language_localname.to_dict())


@pytest.fixture()
def sample_language_schema(sample_language: Language):
    return LanguageSchema.from_dict(sample_language.to_dict())


@pytest.fixture()
def sample_type_schema(sample_type: Type):
    return TypeSchema.from_dict(sample_type.to_dict())


@pytest.fixture()
def sample_related_schema():
    return RelatedSchema(related_id=1835927)


@pytest.fixture()
def sample_scene_index_schema():
    return SceneIndexSchema(scene_index=1)


@pytest.fixture()
def sample_galleryinfo_schema(sample_galleryinfo: Galleryinfo):
    return GalleryinfoSchema.from_dict(sample_galleryinfo.to_dict())
