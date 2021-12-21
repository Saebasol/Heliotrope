from sanic_testing.manager import TestManager  # type:ignore

url = "/api/hitomi/image/"


def test_image(app: TestManager):
    _, response = app.test_client.get(url + "1613730")
    assert response.status == 200


def test_image_not_found(app: TestManager):
    _, response = app.test_client.get(url + "0")
    assert response.status == 404
