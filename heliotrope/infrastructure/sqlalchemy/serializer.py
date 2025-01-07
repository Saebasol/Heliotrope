from typing import Any
from heliotrope.core.serializer import Serializer


class SchemaSerializer(Serializer):
    def _dict_factory(self, data: Any):
        serialized = super()._dict_factory(data)
        if serialized.get("related"):
            serialized["related"] = [
                related["related_id"] for related in serialized["related"]
            ]
        if serialized.get("scene_indexes"):
            serialized["scene_indexes"] = [
                scene_index["scene_index"]
                for scene_index in serialized["scene_indexes"]
            ]

        if "id" in serialized and "galleryinfo_id" in serialized:
            del serialized["id"]
            del serialized["galleryinfo_id"]
        return serialized
