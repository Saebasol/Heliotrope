from heliotrope.application.dtos.thumbnail import Size
from heliotrope.application.javascript.interpreter import JavaScriptInterpreter
from heliotrope.domain.entities.file import File


class ThumbnailResolver:
    def __init__(self, js_interpreter: JavaScriptInterpreter) -> None:
        self.js_interpreter = js_interpreter
        self._avif_resolver = AVIFThumbnailResolver(js_interpreter)
        self._webp_resolver = WebPThumbnailResolver(js_interpreter)

    @property
    def avif(self) -> "AVIFThumbnailResolver":
        return self._avif_resolver

    @property
    def webp(self) -> "WebPThumbnailResolver":
        return self._webp_resolver

    def get_thumbnail_url(self, galleryid: int, image: File, size: Size) -> str:
        if size == Size.SMALLSMALL:
            return self.get_smallsmall_thumbnail(galleryid, image)
        elif size == Size.SMALL:
            return self.get_small_thumbnail(galleryid, image)
        elif size == Size.SMALLBIG:
            return self.get_smallbig_thumbnail(galleryid, image)
        elif size == Size.BIG:
            return self.get_big_thumbnail(galleryid, image)

    def get_smallsmall_thumbnail(self, galleryid: int, image: File) -> str:
        if image.hasavif:
            return self._avif_resolver.get_avif_smallsmall_thumbnail(galleryid, image)

        return self._webp_resolver.get_webp_smallsmall_thumbnail(galleryid, image)

    def get_small_thumbnail(self, galleryid: int, image: File) -> str:
        if image.hasavif:
            return self._avif_resolver.get_avif_small_thumbnail(galleryid, image)

        return self._webp_resolver.get_webp_small_thumbnail(galleryid, image)

    def get_smallbig_thumbnail(self, galleryid: int, image: File) -> str:
        if image.hasavif:
            return self._avif_resolver.get_avif_smallbig_thumbnail(galleryid, image)

        return self._webp_resolver.get_webp_smallbig_thumbnail(galleryid, image)

    def get_big_thumbnail(self, galleryid: int, image: File) -> str:
        if image.hasavif:
            return self._avif_resolver.get_avif_big_thumbnail(galleryid, image)

        return self._webp_resolver.get_webp_big_thumbnail(galleryid, image)


class AVIFThumbnailResolver:
    def __init__(self, js_interpreter: JavaScriptInterpreter) -> None:
        self.js_interpreter = js_interpreter
        self.ext = "avif"

    def get_avif_smallsmall_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "smallsmalltn", self.ext, "tn"
        )

    def get_avif_small_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "smalltn", self.ext, "tn"
        )

    def get_avif_smallbig_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "smallbigtn", self.ext, "tn"
        )

    def get_avif_big_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "bigtn", self.ext, "tn"
        )


class WebPThumbnailResolver:
    def __init__(self, js_interpreter: JavaScriptInterpreter) -> None:
        self.js_interpreter = js_interpreter
        self.ext = "webp"

    def get_webp_smallsmall_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "smallsmalltn", self.ext, "tn"
        )

    def get_webp_small_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "smalltn", self.ext, "tn"
        )

    def get_webp_smallbig_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "smallbigtn", self.ext, "tn"
        )

    def get_webp_big_thumbnail(self, galleryid: int, image: File) -> str:
        return self.js_interpreter.url_from_url_from_hash(
            galleryid, image, self.ext + "bigtn", self.ext, "tn"
        )
