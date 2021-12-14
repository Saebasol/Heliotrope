from sanic_testing.manager import TestManager  # type:ignore

url = "/api/hitomi/info/"


def test_info(app: TestManager):
    _, response = app.test_client.get(url + "1613730")
    assert response.status == 200


def test_info_not_in_db(app: TestManager):
    _, response = app.test_client.get(url + "902349")
    assert response.status == 200


def test_info_not_found(app: TestManager):
    _, response = app.test_client.get(url + "0")
    assert response.status == 404
