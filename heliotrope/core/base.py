from __future__ import annotations

from heliotrope.core.deserializer import Deserializer
from heliotrope.core.serializer import Serializer


class BaseHeliotrope: ...


class HeliotropeEntity(BaseHeliotrope, Serializer, Deserializer): ...
