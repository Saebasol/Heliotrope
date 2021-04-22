def test_get_list_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/list/1")
    assert response.status == 200


def test_get_list_raw_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/list/1?raw=true")
    assert response.status == 200


def test_get_list_not_found_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/list/0")
    assert response.status == 404
