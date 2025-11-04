from yggdrasil.domain.entities.file import File
from yggdrasil.domain.entities.resolved_image import ResolvedImage


def test_resolved_image_creation():
    file = File(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    resolved_image = ResolvedImage(url="http://example.com/image.jpg", file=file)

    assert resolved_image.url == "http://example.com/image.jpg"
    assert isinstance(resolved_image.file, File)
    assert resolved_image.file.hash == "test_hash"


def test_resolved_image_serialization():
    file = File(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    resolved_image = ResolvedImage(url="http://example.com/image.jpg", file=file)

    result = resolved_image.to_dict()

    assert result["url"] == "http://example.com/image.jpg"
    assert "file" in result
    assert result["file"]["hash"] == "test_hash"


def test_resolved_image_deserialization():
    resolved_image = ResolvedImage.from_dict(
        {
            "url": "http://example.com/image.jpg",
            "file": {
                "hasavif": True,
                "hash": "test_hash",
                "height": 1080,
                "name": "test.jpg",
                "width": 1920,
                "hasjxl": False,
                "haswebp": False,
                "single": False,
            },
        }
    )

    assert resolved_image.url == "http://example.com/image.jpg"
    assert isinstance(resolved_image.file, File)
    assert resolved_image.file.hash == "test_hash"


def test_resolved_image_equality():
    file = File(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )

    resolved_image1 = ResolvedImage(url="http://example.com/image.jpg", file=file)
    resolved_image2 = ResolvedImage(url="http://example.com/image.jpg", file=file)

    different_file = File(
        hasavif=False,
        hash="different_hash",
        height=720,
        name="different.jpg",
        width=1280,
    )
    resolved_image3 = ResolvedImage(
        url="http://different.com/image.jpg", file=different_file
    )

    assert resolved_image1 == resolved_image2
    assert resolved_image1 != resolved_image3
