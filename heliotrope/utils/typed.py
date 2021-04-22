from types import SimpleNamespace
from typing import TYPE_CHECKING, Literal, Optional, TypedDict

from sanic.app import Sanic
from sanic.request import Request

if TYPE_CHECKING:
    from heliotrope.mirroring import Mirroring
    from heliotrope.utils.requester import HitomiRequester


class Files(TypedDict):
    width: int
    hash: str
    haswebp: int
    name: str
    height: int


class Tags(TypedDict):
    male: Literal["", "1"]
    female: Literal["", "1"]
    url: str
    tag: str


class GalleryInfoJSON(TypedDict):
    language_localname: str
    language: str
    date: str
    files: list[Files]
    tags: list[Tags]
    japanese_title: Optional[str]
    title: str
    id: str
    type: str


class HeliotropeContext(SimpleNamespace):
    hitomi_requester: "HitomiRequester"
    mirroring_manager: "Mirroring"


class Heliotrope(Sanic):
    ctx: HeliotropeContext


class HeliotropeRequest(Request):
    app: Heliotrope
