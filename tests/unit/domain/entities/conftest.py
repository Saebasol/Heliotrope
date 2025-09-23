from datetime import date, datetime

import pytest

from heliotrope.domain.entities.artist import Artist
from heliotrope.domain.entities.character import Character
from heliotrope.domain.entities.file import File
from heliotrope.domain.entities.galleryinfo import Galleryinfo
from heliotrope.domain.entities.group import Group
from heliotrope.domain.entities.info import Info
from heliotrope.domain.entities.language import Language
from heliotrope.domain.entities.language_info import LanguageInfo
from heliotrope.domain.entities.language_localname import LanguageLocalname
from heliotrope.domain.entities.parody import Parody
from heliotrope.domain.entities.raw_galleryinfo import RawGalleryinfo
from heliotrope.domain.entities.raw_language import RawLanguage
from heliotrope.domain.entities.resolved_image import ResolvedImage
from heliotrope.domain.entities.tag import Tag
from heliotrope.domain.entities.type import Type


@pytest.fixture()
def sample_artist():
    return Artist(artist="tamano kedama", url="/artist/tamano%20kedama-all.html")


@pytest.fixture()
def sample_character():
    return Character(character="sutora", url="/character/sutora-all.html")


@pytest.fixture()
def sample_file():
    return File(
        hasavif=True,
        hash="537a414e4e381db417537992468b576c1ba543f2cb82f63f07628d1f0eb4847f",
        height=1821,
        name="001.jpg",
        width=1290,
        hasjxl=False,
        haswebp=True,
        single=False,
    )


@pytest.fixture()
def sample_group():
    return Group(group="kedama gyuunyuu", url="/group/kedama%20gyuunyuu-all.html")


@pytest.fixture()
def sample_parody():
    return Parody(parody="original", url="/series/original-all.html")


@pytest.fixture()
def sample_tag():
    return Tag(
        tag="digital",
        url="/tag/digital-all.html",
        female=False,
        male=False,
    )


@pytest.fixture()
def sample_tag_male():
    return Tag(tag="shota", url="/tag/male%3Ashota-all.html", female=False, male=True)


@pytest.fixture()
def sample_tag_female():
    return Tag(tag="loli", url="/tag/female%3Aloli-all.html", female=True, male=False)


@pytest.fixture()
def sample_language_info():
    return LanguageInfo(language="japanese", language_url="/index-japanese.html")


@pytest.fixture()
def sample_language_localname():
    return LanguageLocalname(name="日本語")


@pytest.fixture()
def sample_language(
    sample_language_info: LanguageInfo,
    sample_language_localname: LanguageLocalname,
):
    return Language(
        galleryid=2639954,
        url="/galleries/2639954.html",
        language_localname=sample_language_localname,
        language_info=sample_language_info,
    )


@pytest.fixture()
def sample_type():
    return Type(type="manga")


@pytest.fixture()
def sample_resolved_image(sample_file: File):
    return ResolvedImage(url="http://example.com/image.jpg", file=sample_file)


@pytest.fixture()
def sample_raw_language():
    return RawLanguage(
        galleryid=2639954,
        language_localname="日本語",
        name="japanese",
        url="/galleries/2639954.html",
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
        date=datetime(2023, 8, 12, 10, 10),
        galleryurl="/doujinshi/全部君のせいだ。総集編-extra-日本語-2639954.html",
        id=2639954,
        japanese_title="全部君のせいだ。総集編 EXTRA",
        language_localname="日本語",
        language_url="/index-japanese.html",
        language="japanese",
        title="Zenbu Kimi no Sei da. Soushuuhen EXTRA",
        type="doujinshi",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 8, 13),
        artists=[sample_artist],
        characters=[sample_character],
        files=[sample_file],
        groups=[sample_group],
        languages=[sample_raw_language],
        parodys=[sample_parody],
        related=[1835927, 1815701, 2169403, 1417083, 2614236],
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
        date=datetime(2023, 8, 12, 10, 10),
        galleryurl="/doujinshi/全部君のせいだ。総集編-extra-日本語-2639954.html",
        id=2639954,
        japanese_title="全部君のせいだ。総集編 EXTRA",
        title="Zenbu Kimi no Sei da. Soushuuhen EXTRA",
        video=None,
        videofilename=None,
        blocked=False,
        datepublished=date(2023, 8, 13),
        type=sample_type,
        language_localname=sample_language_localname,
        language_info=sample_language_info,
        artists=[sample_artist],
        characters=[sample_character],
        files=[sample_file],
        groups=[sample_group],
        languages=[sample_language],
        parodys=[sample_parody],
        related=[1835927, 1815701, 2169403, 1417083, 2614236],
        scene_indexes=[1, 2, 3],
        tags=[sample_tag],
    )


@pytest.fixture()
def sample_info():
    return Info(
        id=2639954,
        title="Zenbu Kimi no Sei da. Soushuuhen EXTRA",
        artists=["tamano_kedama"],
        groups=["kedama_gyuunyuu"],
        type="doujinshi",
        language="japanese",
        series=["original"],
        characters=["sutora"],
        tags=[
            "female:beauty_mark",
            "female:blowjob",
            "female:bondage",
            "female:collar",
            "female:crotch_tattoo",
            "male:dark_skin",
            "female:demon_girl",
            "tag:digital",
            "male:dilf",
            "female:filming",
            "female:footjob",
            "male:glasses",
            "female:loli",
            "female:mesugaki",
            "female:pantyhose",
            "female:schoolgirl_uniform",
            "male:shota",
            "female:sole_female",
            "tag:soushuuhen",
            "male:teacher",
            "female:twintails",
            "female:unusual_pupils",
            "female:x-ray",
        ],
        date=datetime(2023, 8, 12, 10, 10),
    )
