from pytest import mark

from heliotrope.sanic import Heliotrope

url = "/api/proxy/"


@mark.flaky(reruns=3, reruns_delay=5)
def test_proxy_hitomi(app: Heliotrope, image_url: str):
    _, response = app.test_client.get(url + image_url)
    assert response.status == 200


def test_proxy_pixiv(app: Heliotrope):
    image_url = "https://i.pximg.net/img-master/img/2020/01/28/01/07/34/79136250_p0_master1200.jpg"
    _, response = app.test_client.get(url + image_url)
    assert response.status == 200


def test_proxy_invalid(app: Heliotrope):
    _, response = app.test_client.get(url + "test")
    assert response.status == 400


def test_proxy_not_found(app: Heliotrope):
    image_url = "https://i.pximg.net/img-master/img/1234/56/78/91/07/34/7312310_p0_master1200.jpg"
    _, response = app.test_client.get(url + image_url)
    assert response.status == 404
