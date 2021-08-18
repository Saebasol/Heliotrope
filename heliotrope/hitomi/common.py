# https://ltn.hitomi.la/common.js

import re
from math import isnan
from typing import Optional

from heliotrope.hitomi.models import HitomiFiles


def subdomain_from_galleryid(g: int, number_of_frontends: int) -> str:
    o = g % number_of_frontends
    return chr(97 + o)


def subdomain_from_url(url: str, base: Optional[str] = None) -> str:
    retval = "b"

    if base:
        retval = base

    # number_of_frontends = 3
    b = 16

    r = re.compile(r"\/[0-9a-f]\/([0-9a-f]{2})\/")
    m = r.search(url)

    if not m:
        return "a"

    g = int(m[1], b)

    if not isnan(g):
        o = 0
        if g < 0x88:
            o = 1

        if g < 0x44:
            o = 2

        # retval = subdomain_from_galleryid(g, number_of_frontends) + retval
        retval = chr(97 + o) + retval

    return retval


def url_from_url(url: str, base: Optional[str] = None) -> str:
    return re.sub(
        r"\/\/..?\.hitomi\.la\/",
        "//" + subdomain_from_url(url, base) + ".hitomi.la/",
        url,
    )


def full_path_from_hash(hash: str) -> str:
    if len(hash) < 3:
        return hash

    return re.sub(r"^.*(..)(.)$", r"\2/\1/" + hash, hash)


def url_from_hash(
    galleryid: int,
    image: HitomiFiles,
    dir: Optional[str] = None,
    ext: Optional[str] = None,
) -> str:
    ext = ext or dir or image.name.split(".")[-1]
    dir = dir or "images"

    return (
        "https://a.hitomi.la/" + dir + "/" + full_path_from_hash(image.hash) + "." + ext
    )


def url_from_url_from_hash(
    galleryid: int,
    image: HitomiFiles,
    dir: Optional[str] = None,
    ext: Optional[str] = None,
    base: Optional[str] = None,
) -> str:
    return url_from_url(url_from_hash(galleryid, image, dir, ext), base)


def image_url_from_image(galleryid: int, image: HitomiFiles, no_webp: bool) -> str:
    webp = None
    if image.hash and image.haswebp and not no_webp:
        webp = "webp"

    return url_from_url_from_hash(galleryid, image, webp)
