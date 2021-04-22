def test_get_info_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/info/1536576")
    assert response.status == 200


def test_get_info_not_found_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/info/0")
    assert response.status == 404
