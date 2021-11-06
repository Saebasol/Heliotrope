from heliotrope.domain.tag import HitomiTag
from heliotrope.types import HitomiTagJSON

hitomi_tag_include_dict: HitomiTagJSON = {
    "male": "",
    "female": "1",
    "tag": "big breasts",
    "url": "/tag/female%3Abig%20breasts-all.html",
}


def test_hitomi_tag_model_init():
    hitomi_tag = HitomiTag(
        male="",
        female="1",
        tag="big breasts",
        url="/tag/female%3Abig%20breasts-all.html",
    )

    assert hitomi_tag.male == ""
    assert hitomi_tag.female == "1"
    assert hitomi_tag.tag == "big breasts"
    assert hitomi_tag.url == "/tag/female%3Abig%20breasts-all.html"


def test_hitomi_tag_model_from_dict():
    hitomi_tag = HitomiTag.from_dict(hitomi_tag_include_dict)

    assert hitomi_tag.male == ""
    assert hitomi_tag.female == "1"
    assert hitomi_tag.tag == "big breasts"
    assert hitomi_tag.url == "/tag/female%3Abig%20breasts-all.html"


def test_hitomi_tag_model_to_dict_include_male_female():
    hitomi_tag = HitomiTag.from_dict(hitomi_tag_include_dict)

    assert hitomi_tag_include_dict == hitomi_tag.to_dict()


def test_hitomi_tag_model_to_dict_exclude_male_female():
    hitomi_tag_exclude_dict: HitomiTagJSON = {
        "tag": "no penetration",
        "url": "/tag/no%20penetration-all.html",
    }

    hitomi_tag = HitomiTag.from_dict(hitomi_tag_exclude_dict)

    assert hitomi_tag_exclude_dict == hitomi_tag.to_dict()


def test_hitomi_tag_model_comparison():
    hitomi_tag1 = HitomiTag.from_dict(hitomi_tag_include_dict)
    hitomi_tag2 = HitomiTag.from_dict(hitomi_tag_include_dict)

    assert hitomi_tag1 == hitomi_tag2
