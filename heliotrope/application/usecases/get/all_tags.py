from typing import Generator

from heliotrope.domain.entities.all_tags import AllTags
from heliotrope.domain.repositories.artist import ArtistRepository
from heliotrope.domain.repositories.character import CharacterRepository
from heliotrope.domain.repositories.group import GroupRepository
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.domain.repositories.parody import ParodyRepository
from heliotrope.domain.repositories.tag import TagRepository
from heliotrope.domain.repositories.type import TypeRepository


def replace(name: str) -> str:
    return name.replace(" ", "_")


class GetAllTagsUseCase:
    def __init__(
        self,
        artist_repository: ArtistRepository,
        character_repository: CharacterRepository,
        group_repository: GroupRepository,
        language_info_repository: LanguageInfoRepository,
        parody_repository: ParodyRepository,
        tag_repository: TagRepository,
        type_repository: TypeRepository,
    ) -> None:
        self.artist_repository = artist_repository
        self.character_repository = character_repository
        self.group_repository = group_repository
        self.language_info_repository = language_info_repository
        self.parody_repository = parody_repository
        self.tag_repository = tag_repository
        self.type_repository = type_repository

    def __await__(self) -> Generator[None, None, AllTags]:
        return self.execute().__await__()

    async def execute(self) -> AllTags:
        artists = await self.artist_repository.get_all_artists()
        characters = await self.character_repository.get_all_characters()
        groups = await self.group_repository.get_all_groups()
        language_infos = await self.language_info_repository.get_all_language_infos()
        parodies = await self.parody_repository.get_all_parodies()
        tags = await self.tag_repository.get_all_tags()
        types = await self.type_repository.get_all_types()

        tag_list: list[str] = []
        female_list: list[str] = []
        male_list: list[str] = []
        for tag in tags:
            if tag[1] is False and tag[2] is False:
                tag_list.append(replace(tag[0]))
            elif tag[1] is True and tag[2] is False:
                male_list.append(replace(tag[0]))
            elif tag[1] is False and tag[2] is True:
                female_list.append(replace(tag[0]))

        return AllTags(
            artists=[replace(artist) for artist in artists],
            characters=[replace(character) for character in characters],
            groups=[replace(group) for group in groups],
            language=[replace(language_info) for language_info in language_infos],
            series=[replace(parody) for parody in parodies],
            tag=tag_list,
            female=female_list,
            male=male_list,
            type=[replace(type) for type in types],
        )
