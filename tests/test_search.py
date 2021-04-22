def test_get_search_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/search?q=sekigahara")
    assert response.status == 200


def test_get_search_raw_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/search?q=sekigahara&raw=true")
    assert response.status == 200


def test_get_search_not_found_response(app):
    _, response = app.test_client.get("/v4/api/hitomi/search?q=testqueryxd")
    assert response.status == 404
