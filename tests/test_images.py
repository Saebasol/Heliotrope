def test_get_images_not_in_database_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/images/1")
    assert response.status == 200


def test_get_images_in_database_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/images/1536576")
    assert response.status == 200


def test_get_images_not_found_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/images/0")
    assert response.status == 404
