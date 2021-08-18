from sanic_testing.manager import TestManager  # type:ignore

url = "/v5/api/proxy/"


def test_proxy_hitomi(app: TestManager):
    _, response = app.test_client.get(
        url
        + "bb_images_hitomi_la_5_6c_0d2ee87048646232b205bdf1da11240542178c0c58473beb40461aa51d6ee6c5.jpg"
    )
    assert response.status == 200


def test_proxy_pixiv_original(app: TestManager):
    _, response = app.test_client.get(
        url + "i_img-original_pximg_net_img_2020_01_28_01_07_34_79136250_p0.jpg"
    )
    assert response.status == 200


def test_proxy_pixiv_master(app: TestManager):
    _, response = app.test_client.get(
        url
        + "i_img-master_pximg_net_img_2020_01_28_01_07_34_79136250_p0_master1200.jpg"
    )
    assert response.status == 200


def test_proxy_bad_request(app: TestManager):
    _, response = app.test_client.get(
        url
        + "i_img-master_pximg_net_img_1234_56_78_09_10_11_12131415_p0_master1200.jpg"
    )
    assert response.status == 400
    _, response = app.test_client.get(url + "test.jpg")
    assert response.status == 400
