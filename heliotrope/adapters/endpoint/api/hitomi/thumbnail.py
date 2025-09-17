from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.types import Schema

from heliotrope.application.dtos.thumbnail import GetThumbnailQueryDTO, Size
from heliotrope.application.usecases.get.galleryinfo import GetGalleryinfoUseCase
from heliotrope.application.usecases.get.resolved_image import (
    GetResolvedThumbnailUseCase,
)
from heliotrope.application.utils import check_int32
from heliotrope.domain.exceptions import GalleryinfoNotFound
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_thumbnail = Blueprint("hitomi_thumbnail", url_prefix="/thumbnail")


class HitomiThumbnailView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la thumbnail")
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="id", location="path", schema=int, required=True
    )
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="size",
        location="query",
        schema=Size,
        required=True,
    )
    @openapi.parameter(  # pyright: ignore[reportUnknownMemberType]
        name="single",
        location="query",
        schema=Schema.make(  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
            bool, default=True
        ),
    )
    @validate(query=GetThumbnailQueryDTO, query_argument="query")
    async def get(
        self,
        request: HeliotropeRequest,
        id: int,
        query: GetThumbnailQueryDTO,
    ) -> HTTPResponse:
        check_int32(id)
        try:
            galleryinfo = await GetGalleryinfoUseCase(
                request.app.ctx.sa_galleryinfo_repository
            ).execute(id)
        except GalleryinfoNotFound:
            galleryinfo = await GetGalleryinfoUseCase(
                request.app.ctx.hitomi_la_galleryinfo_repository
            ).execute(id)
        if query.single == "true":
            return json(
                [
                    GetResolvedThumbnailUseCase(
                        request.app.ctx.pythonmonkey_resolved_image_repository
                    )
                    .execute(galleryinfo.id, galleryinfo.files[0], query.size)
                    .to_dict()
                ]
            )

        return json(
            [
                GetResolvedThumbnailUseCase(
                    request.app.ctx.pythonmonkey_resolved_image_repository
                )
                .execute(galleryinfo.id, file, query.size)
                .to_dict()
                for file in galleryinfo.files
            ]
        )


hitomi_thumbnail.add_route(HitomiThumbnailView.as_view(), "/<id:int>")
