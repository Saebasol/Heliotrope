from yggdrasil.domain.entities.file import File


def test_file_creation():
    file = File(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    assert file.hasavif is True
    assert file.hash == "test_hash"
    assert file.height == 1080
    assert file.name == "test.jpg"
    assert file.width == 1920
    assert file.hasjxl is False
    assert file.haswebp is False
    assert file.single is False


def test_file_serialization():
    file = File(
        hasavif=True,
        hash="test_hash",
        height=1080,
        name="test.jpg",
        width=1920,
        hasjxl=True,
        haswebp=True,
        single=True,
    )
    assert {
        "hasavif": True,
        "hash": "test_hash",
        "height": 1080,
        "name": "test.jpg",
        "width": 1920,
        "hasjxl": True,
        "haswebp": True,
        "single": True,
    } == file.to_dict()


def test_file_deserialization():
    file = File.from_dict(
        {
            "hasavif": True,
            "hash": "test_hash",
            "height": 1080,
            "name": "test.jpg",
            "width": 1920,
            "hasjxl": True,
            "haswebp": True,
            "single": True,
        }
    )
    assert file.hasavif is True
    assert file.hash == "test_hash"
    assert file.height == 1080
    assert file.name == "test.jpg"
    assert file.width == 1920
    assert file.hasjxl is True
    assert file.haswebp is True
    assert file.single is True


def test_file_equality():
    file1 = File(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    file2 = File(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    file3 = File(
        hasavif=False,
        hash="different_hash",
        height=720,
        name="different.jpg",
        width=1280,
    )
    assert file1 == file2
    assert file1 != file3
