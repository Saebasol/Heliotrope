from heliotrope.domain.file import HitomiFile
from heliotrope.types import HitomiFileJSON


hitomi_file_exclude_dict: HitomiFileJSON = {
    "width": 212,
    "hash": "0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5",
    "haswebp": 1,
    "name": "01.jpg",
    "height": 300,
}


def test_hitomi_file_model_init():
    hitomi_file = HitomiFile(
        width=212,
        hash="0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5",
        haswebp=1,
        name="01.jpg",
        height=300,
    )

    assert hitomi_file.width == 212
    assert (
        hitomi_file.hash
        == "0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5"
    )
    assert hitomi_file.haswebp == 1
    assert hitomi_file.name == "01.jpg"
    assert hitomi_file.height == 300


def test_hitomi_file_model_from_dict():
    hitomi_file = HitomiFile.from_dict(hitomi_file_exclude_dict)

    assert hitomi_file.width == 212
    assert (
        hitomi_file.hash
        == "0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5"
    )
    assert hitomi_file.haswebp == 1
    assert hitomi_file.name == "01.jpg"
    assert hitomi_file.height == 300


def test_hitomi_file_model_to_dict_include_hasavif_hasavifsmalltn():
    hitomi_file_include_dict: HitomiFileJSON = {
        "width": 212,
        "hash": "0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5",
        "haswebp": 1,
        "name": "01.jpg",
        "height": 300,
        "hasavif": 1,
        "hasavifsmalltn": 1,
    }
    hitomi_file = HitomiFile.from_dict(hitomi_file_include_dict)

    assert hitomi_file_include_dict == hitomi_file.to_dict()


def test_hitomi_file_model_to_dict_exclude_hasavif_hasavifsmalltn():
    hitomi_file = HitomiFile.from_dict(hitomi_file_exclude_dict)

    assert hitomi_file_exclude_dict == hitomi_file.to_dict()


def test_hitomi_file_model_comparison():
    hitomi_file1 = HitomiFile.from_dict(hitomi_file_exclude_dict)
    hitomi_file2 = HitomiFile.from_dict(hitomi_file_exclude_dict)

    assert hitomi_file1.to_dict() == hitomi_file2.to_dict()
