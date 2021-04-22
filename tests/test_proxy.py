def test_get_proxy_hitomi_response(app):
    _, response = app.test_client.get(
        "/v4/api/proxy/ab_images_hitomi_la_d_2c_85663460c1789a1c9dcd79f8e3f00cdfcf50c5c8248135457006f54a74fdc2cd.jpg"
    )
    assert response.status == 200


def test_get_proxy_pixiv_response(app):
    _, response = app.test_client.get(
        "/v4/api/proxy/i_img-original_pximg_net_img_2020_01_28_01_07_34_79136250_p0.jpg"
    )
    assert response.status == 200


def test_get_proxy_bad_request_response(app):
    _, response = app.test_client.get("/v4/api/proxy/test")
    assert response.status == 400
