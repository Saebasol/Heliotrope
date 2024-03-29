from math import isnan
from re import compile, sub
from typing import cast

from heliotrope.domain import File, Info
from heliotrope.js.gg import GG


class Common:
    def __init__(self, gg: GG) -> None:
        self.gg = gg

    @classmethod
    def setup(cls, code: str) -> "Common":
        gg = GG(code)
        gg.parse()
        return cls(gg)

    def subdomain_from_url(self, url: str, base: str) -> str:
        retval = "b"
        if base:
            retval = base

        b = 16

        r = compile(r"\/[0-9a-f]{61}([0-9a-f]{2})([0-9a-f])")
        m = r.search(url)

        if not m:
            return "a"

        g = int(m[2] + m[1], b)

        if not isnan(g):
            retval = chr(97 + self.gg.m(g)) + retval

        return retval

    def url_from_url(self, url: str, base: str) -> str:
        return sub(
            r"\/\/..?\.hitomi\.la\/",
            "//" + self.subdomain_from_url(url, base) + ".hitomi.la/",
            url,
        )

    def full_path_from_hash(self, hash: str) -> str:
        return self.gg.b + self.gg.s(hash) + "/" + hash

    def real_full_path_from_hash(self, hash: str) -> str:
        return sub(r"^.*(..)(.)$", r"\2/\1/" + hash, hash)

    def url_from_hash(self, galleryid: str, image: File, dir: str, ext: str) -> str:
        ext = ext or dir or image.name.split(".").pop()
        dir = dir or "images"
        return (
            "https://a.hitomi.la/"
            + dir
            + "/"
            + self.full_path_from_hash(image.hash)
            + "."
            + ext
        )

    def url_from_url_from_hash(
        self, galleryid: str, image: File, dir: str, ext: str, base: str
    ) -> str:
        if "tn" == base:
            return self.url_from_url(
                "https://a.hitomi.la/"
                + dir
                + "/"
                + self.real_full_path_from_hash(image.hash)
                + "."
                + ext,
                base,
            )

        return self.url_from_url(self.url_from_hash(galleryid, image, dir, ext), base)

    def rewrite_tn_paths(self, html: str) -> str:
        return sub(
            r"//tn\.hitomi\.la/[^/]+/[0-9a-f]/[0-9a-f]{2}/[0-9a-f]{64}",
            lambda url: self.url_from_url(url.group(0), "tn"),
            html,
        )

    def get_thumbnail(self, galleryid: str, image: File) -> str:
        return self.url_from_url_from_hash(galleryid, image, "webpbigtn", "webp", "tn")

    def convert_thumbnail(self, info: Info) -> dict[str, str]:
        thumnbnail_url = self.get_thumbnail(str(info.id), info.thumbnail)
        info_dict = cast(dict[str, str], info.to_dict())
        info_dict["thumbnail"] = thumnbnail_url
        return info_dict

    def image_urls(
        self, galleryid: str, images: list[File], no_webp: bool
    ) -> list[str]:
        return [
            self.image_url_from_image(galleryid, image, no_webp) for image in images
        ]

    def image_url_from_image(self, galleryid: str, image: File, no_webp: bool) -> str:
        ext = "webp"
        if image.hasavif:
            ext = "avif"

        return self.url_from_url_from_hash(galleryid, image, ext, "", "a")
