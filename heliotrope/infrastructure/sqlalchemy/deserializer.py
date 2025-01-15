from typing import Any, Mapping, Self, get_type_hints, get_origin, get_args
from heliotrope.core.deserializer import Deserializer
from sqlalchemy.orm import Mapped


class SchemaDeserializer(Deserializer):
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        type_hints = get_type_hints(cls)
        for key, value in type_hints.items():
            if get_origin(value) is Mapped:
                type_hints[key] = get_args(value)[0]

        if cls.__name__.startswith("Related"):
            data = {"related_id": data}
        if cls.__name__.startswith("SceneIndex"):
            data = {"scene_index": data}

        cls.__annotations__ = type_hints

        return super().from_dict(data)
