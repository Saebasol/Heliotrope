from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Serializer:
    def _dict_factory(self, data: Any) -> dict[str, Any]:
        serialized = dict(data)
        if serialized.get("date"):
            serialized["date"] = serialized["date"].isoformat()
        if serialized.get("datepublished"):
            serialized["datepublished"] = serialized["datepublished"].isoformat()
        return serialized

    def to_dict(self) -> dict[str, Any]:
        return asdict(self, dict_factory=self._dict_factory)
