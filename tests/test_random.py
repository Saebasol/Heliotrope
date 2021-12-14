from sanic_testing.manager import TestManager  # type:ignore

url = "/api/hitomi/random"


def test_random(app: TestManager):
    _, response = app.test_client.get(url)
    assert response.status == 200
