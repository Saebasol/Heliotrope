from sanic_testing.manager import TestManager  # type:ignore

url = "/api/hitomi/search"


def test_search(app: TestManager):
    _, response = app.test_client.post(
        url, json={"offset": 1, "query": ["sekigahara", "artist:tsukako"]}
    )
    assert response.status == 200
    assert response.json["count"] == 1


def test_search_not_found(app: TestManager):
    _, response = app.test_client.post(
        url, json={"offset": 1, "query": ["female:loli"]}
    )
    assert response.status == 200
    assert response.json["count"] == 0
