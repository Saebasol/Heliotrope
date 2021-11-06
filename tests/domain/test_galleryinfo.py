from heliotrope.domain.galleryinfo import HitomiGalleryInfo, HitomiFile, HitomiTag
from heliotrope.types import HitomiFileJSON, HitomiGalleryinfoJSON, HitomiTagJSON

tags: list[HitomiTagJSON] = [
    {
        "male": "",
        "female": "1",
        "tag": "big breasts",
        "url": "/tag/female%3Abig%20breasts-all.html",
    },
    {
        "male": "",
        "female": "1",
        "tag": "exhibitionism",
        "url": "/tag/female%3Aexhibitionism-all.html",
    },
]


files: list[HitomiFileJSON] = [
    {
        "width": 212,
        "hash": "0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5",
        "haswebp": 1,
        "name": "01.jpg",
        "height": 300,
    },
    {
        "width": 212,
        "hash": "71aceb04d1f461ba221915f584ef94fcdb05d3effe070fa7753eb1b42f3cc08f",
        "haswebp": 1,
        "name": "02.jpg",
        "height": 300,
    },
]


galleryinfo: HitomiGalleryinfoJSON = {
    "language_localname": "한국어",
    "language": "korean",
    "date": "2020-02-14 07=57=00-06",
    "japanese_title": None,
    "title": "Sekigahara-san wa Tasshitai | 세키가하라는 닿고싶어",
    "id": "1570712",
    "type": "manga",
    "tags": tags,
    "files": files,
}


def test_hitomi_galleryinfo_init():
    hitomi_galleryinfo = HitomiGalleryInfo(
        language_localname="한국어",
        language="korean",
        date="2020-02-14 07=57=00-06",
        japanese_title=None,
        title="Sekigahara-san wa Tasshitai | 세키가하라는 닿고싶어",
        id="1570712",
        type="manga",
        tags=tags,
        files=files,
    )

    assert hitomi_galleryinfo.language_localname == "한국어"
    assert hitomi_galleryinfo.language == "korean"
    assert hitomi_galleryinfo.date == "2020-02-14 07=57=00-06"
    assert hitomi_galleryinfo.japanese_title is None
    assert hitomi_galleryinfo.title == "Sekigahara-san wa Tasshitai | 세키가하라는 닿고싶어"
    assert hitomi_galleryinfo.id == "1570712"
    assert hitomi_galleryinfo.type == "manga"
    assert hitomi_galleryinfo.tags == [HitomiTag.from_dict(tag) for tag in tags]
    assert hitomi_galleryinfo.files == [HitomiFile.from_dict(file) for file in files]


def test_hitomi_galleryinfo_from_dict():
    hitomi_galleryinfo = HitomiGalleryInfo.from_dict(galleryinfo)

    assert hitomi_galleryinfo.language_localname == "한국어"
    assert hitomi_galleryinfo.language == "korean"
    assert hitomi_galleryinfo.date == "2020-02-14 07=57=00-06"
    assert hitomi_galleryinfo.japanese_title is None
    assert hitomi_galleryinfo.title == "Sekigahara-san wa Tasshitai | 세키가하라는 닿고싶어"
    assert hitomi_galleryinfo.id == "1570712"
    assert hitomi_galleryinfo.type == "manga"
    assert hitomi_galleryinfo.tags == [HitomiTag.from_dict(tag) for tag in tags]
    assert hitomi_galleryinfo.files == [HitomiFile.from_dict(file) for file in files]


def test_hitomi_galleryinfo_to_dict():
    hitomi_galleryinfo = HitomiGalleryInfo(
        language_localname="한국어",
        language="korean",
        date="2020-02-14 07=57=00-06",
        japanese_title=None,
        title="Sekigahara-san wa Tasshitai | 세키가하라는 닿고싶어",
        id="1570712",
        type="manga",
        tags=tags,
        files=files,
    )

    assert hitomi_galleryinfo.to_dict() == galleryinfo


def test_hitomi_galleryinfo_comparsion():
    hitomi_galleryinfo1 = HitomiGalleryInfo.from_dict(galleryinfo)
    hitomi_galleryinfo2 = HitomiGalleryInfo.from_dict(galleryinfo)

    assert hitomi_galleryinfo1 == hitomi_galleryinfo2
