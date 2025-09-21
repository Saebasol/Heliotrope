from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext.extensions.openapi import openapi

from heliotrope.application.usecases.get.all_tags import GetAllTagsUseCase
from heliotrope.infrastructure.sanic.app import HeliotropeRequest

hitomi_tags = Blueprint("hitomi_tags", url_prefix="/tags")


class HitomiTagsView(HTTPMethodView):
    @openapi.tag("Hitomi")
    @openapi.summary("Get hitomi.la tags")
    async def get(
        self,
        request: HeliotropeRequest,
    ) -> HTTPResponse:
        tags = await GetAllTagsUseCase(
            request.app.ctx.sa_galleryinfo_repository.artist_repository,
            request.app.ctx.sa_galleryinfo_repository.character_repository,
            request.app.ctx.sa_galleryinfo_repository.group_repository,
            request.app.ctx.sa_galleryinfo_repository.language_info_repository,
            request.app.ctx.sa_galleryinfo_repository.parody_repository,
            request.app.ctx.sa_galleryinfo_repository.tag_repository,
            request.app.ctx.sa_galleryinfo_repository.type_repository,
        )
        return json(tags.to_dict())


hitomi_tags.add_route(HitomiTagsView.as_view(), "")
