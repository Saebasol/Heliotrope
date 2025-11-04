from yggdrasil.infrastructure.sqlalchemy.entities.file import FileSchema


def test_file_schema_creation():
    file = FileSchema(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    assert file.hasavif is True
    assert file.hash == "test_hash"
    assert file.height == 1080
    assert file.name == "test.jpg"
    assert file.width == 1920
    assert file.hasjxl is False  # default value
    assert file.haswebp is False  # default value
    assert file.single is False  # default value


def test_file_schema_serialization():
    file = FileSchema(
        hasavif=True,
        hash="test_hash",
        height=1080,
        name="test.jpg",
        width=1920,
        hasjxl=True,
        haswebp=True,
        single=True,
    )
    serialized = file.to_dict()

    assert "hasavif" in serialized
    assert "hash" in serialized
    assert "height" in serialized
    assert "name" in serialized
    assert "width" in serialized
    assert "hasjxl" in serialized
    assert "haswebp" in serialized
    assert "single" in serialized
    assert serialized["hasavif"] is True
    assert serialized["hash"] == "test_hash"
    assert serialized["height"] == 1080
    assert serialized["name"] == "test.jpg"
    assert serialized["width"] == 1920


def test_file_schema_deserialization():
    data = {
        "hasavif": True,
        "hash": "test_hash",
        "height": 1080,
        "name": "test.jpg",
        "width": 1920,
        "hasjxl": True,
        "haswebp": True,
        "single": True,
    }
    file = FileSchema.from_dict(data)

    assert file.hasavif is True
    assert file.hash == "test_hash"
    assert file.height == 1080
    assert file.name == "test.jpg"
    assert file.width == 1920
    assert file.hasjxl is True
    assert file.haswebp is True
    assert file.single is True


def test_file_schema_equality():
    file1 = FileSchema(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    file2 = FileSchema(
        hasavif=True, hash="test_hash", height=1080, name="test.jpg", width=1920
    )
    file3 = FileSchema(
        hasavif=False,
        hash="different_hash",
        height=720,
        name="different.jpg",
        width=1280,
    )

    assert file1 == file2
    assert file1 != file3
