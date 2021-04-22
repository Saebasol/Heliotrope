def test_get_galleryinfo_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/galleryinfo/1536576")
    assert response.status == 200


def test_get_raw_galleryinfo_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/galleryinfo/1536576?raw=True")
    assert response.status == 200


def test_get_galleryinfo_not_found_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/galleryinfo/0")
    assert response.status == 404
