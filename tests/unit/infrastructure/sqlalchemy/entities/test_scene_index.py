from yggdrasil.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema


def test_scene_index_schema_creation():
    scene_index = SceneIndexSchema(scene_index=5)
    assert scene_index.scene_index == 5


def test_scene_index_schema_equality():
    scene_index1 = SceneIndexSchema(scene_index=5)
    scene_index2 = SceneIndexSchema(scene_index=5)
    scene_index3 = SceneIndexSchema(scene_index=10)

    assert scene_index1.scene_index == scene_index2.scene_index
    assert scene_index1.scene_index != scene_index3.scene_index


def test_scene_index_schema_attributes():
    scene_index = SceneIndexSchema(scene_index=5)

    # Test that all required attributes exist
    assert hasattr(scene_index, "scene_index")
    assert hasattr(scene_index, "id")  # From ForeignKeySchema base class
    assert hasattr(scene_index, "galleryinfo_id")  # From ForeignKeySchema base class

    # Test attribute types
    assert isinstance(scene_index.scene_index, int)
