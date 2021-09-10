from heliotrope.hitomi.common import rewrite_tn_paths  # type:ignore


def test_rewrite_tn_paths():
    url = rewrite_tn_paths(
        "//tn.hitomi.la/smallbigtn/5/6c/0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5.jpg"
    )
    assert (
        url
        == "//btn.hitomi.la/smallbigtn/5/6c/0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5.jpg"
    )
