from sanic_testing.manager import TestManager  # type:ignore

url = "/api/hitomi/list/"


def test_list(app: TestManager):
    _, response = app.test_client.get(url + "1")
    assert response.status == 200


def test_list_bad_reqeust(app: TestManager):
    _, response = app.test_client.get(
        url + "999999999999999999999999999999999999999999999999"
    )
    assert response.status == 400
