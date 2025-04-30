from typing import Any

from heliotrope.domain.serializer import Serializer


class SchemaSerializer(Serializer):
    def _dict_factory(self, data: Any) -> dict[str, Any]:
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

        keys_to_remove = [key for key in list(serialized.keys()) if key.startswith("_")]
        for key in keys_to_remove:
            del serialized[key]

        if "type_id" in serialized:
            del serialized["type_id"]
        if "language_info_id" in serialized:
            del serialized["language_info_id"]
        if "localname_id" in serialized:
            del serialized["localname_id"]

        if "id" in serialized and "galleryinfo_id" in serialized:
            del serialized["id"]
            del serialized["galleryinfo_id"]

        if "id" in serialized and not "title" in serialized:
            del serialized["id"]
        return serialized
