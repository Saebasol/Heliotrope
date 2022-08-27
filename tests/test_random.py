from sanic_testing.manager import TestManager  # type:ignore

url = "/api/hitomi/random"


def test_random(app: TestManager):
    _, response = app.test_client.post(url)
    assert response.status == 200


def test_random_with_query(app: TestManager):
    _, response = app.test_client.post(url, {"query": ["sekigahara", "artist:tsukako"]})
    assert response.status == 200
