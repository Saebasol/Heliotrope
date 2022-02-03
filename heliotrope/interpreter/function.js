// If you continue to call the interpreter's function, it becomes very slow.
// Leave all the work to the interpreter.
// 계속해서 인터프리터의 함수를 호출을할경우 매우 느려집니다.
// 인터프리터에 모든작업을 맡깁니다.
function imageUrls(galleryid, images, no_webp) {
    return images.map(function (image) {
        var webp = null
        if (image.hash && image.haswebp && !no_webp) {
            webp = 'webp'
        }
        return { 'name': image.name, 'url': url_from_url_from_hash(galleryid, image, webp, undefined, "a") }
    })
}
// See https://ltn.hitomi.la/gallery.js
function getThumbnail(galleryid, image) {
    return url_from_url_from_hash(galleryid, image, 'webpbigtn', 'webp', 'tn')
}