# https://ltn.hitomi.la/common.js

import re

from heliotrope.utils.hitomi.models import HitomiImageModel


def subdomain_from_galleryid(g: int, number_of_frontends: int) -> str:
    o = g % number_of_frontends
    r = chr(97 + o)
    return r


def subdomain_from_url(url: str) -> str:
    retval = "b"

    number_of_frontends = 3
    b = 16

    r = re.compile(r"\/[0-9a-f]\/([0-9a-f]{2})\/")

    if m := r.search(url):
        g = int(m[1], b)

        if g < 0x30:
            number_of_frontends = 2

        if g < 0x09:
            g = 1

        retval = subdomain_from_galleryid(g, number_of_frontends) + retval

    return retval


def url_from_url(url: str) -> str:
    r = re.compile(r"\/\/..?\.hitomi\.la\/")
    s = subdomain_from_url(url)
    return r.sub(f"//{s}.hitomi.la/", url)


def full_path_from_hash(hash_: str) -> str:
    if len(hash_) < 3:
        return hash_

    result = hash_[len(hash_) - 3 :]
    a = result[0:2]
    b = result[-1]
    return f"{b}/{a}/" + hash_


def url_from_hash(
    galleryid: int, image: HitomiImageModel, dir_: str = None, ext: str = None
) -> str:
    e = image.name.split(".")[-1]
    if ext:
        e = ext

    d = "images"

    if dir_:
        e = dir_
        d = dir_

    r = full_path_from_hash(image.hash)

    return "https://a.hitomi.la/" + d + "/" + r + "." + e


def url_from_url_from_hash(
    galleryid: int, image: HitomiImageModel, dir_: str = None, ext: str = None
) -> str:
    a = url_from_hash(galleryid, image, dir_, ext)
    b = url_from_url(a)
    return b


def image_url_from_image(galleryid: int, image: HitomiImageModel, no_webp: bool) -> str:
    webp = None
    if image.hash and image.haswebp and not no_webp:
        webp = "webp"

    return url_from_url_from_hash(galleryid, image, webp)
