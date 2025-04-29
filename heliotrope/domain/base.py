from __future__ import annotations

from heliotrope.domain.deserializer import Deserializer
from heliotrope.domain.serializer import Serializer


class BaseHeliotrope: ...


class HeliotropeEntity(BaseHeliotrope, Serializer, Deserializer): ...
