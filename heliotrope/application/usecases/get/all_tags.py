from heliotrope.domain.entities.info import parse_male_female_tag, parse_tags_dict_list
from heliotrope.domain.repositories.artist import ArtistRepository
from heliotrope.domain.repositories.charactor import CharacterRepository
from heliotrope.domain.repositories.group import GroupRepository
from heliotrope.domain.repositories.language_info import LanguageInfoRepository
from heliotrope.domain.repositories.parody import ParodyRepository
from heliotrope.domain.repositories.tag import TagRepository
from heliotrope.domain.repositories.type import TypeRepository


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

    def __await__(self):
        return self.execute().__await__()

    async def execute(self) -> dict[str, list[str]]:
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
            parsed_tag = parse_male_female_tag(tag)
            if parsed_tag.startswith("tag:"):
                tag_list.append(parsed_tag)
            elif parsed_tag.startswith("female:"):
                female_list.append(parsed_tag)
            elif parsed_tag.startswith("male:"):
                male_list.append(parsed_tag)

        return {
            "artists": parse_tags_dict_list([artist.to_dict() for artist in artists]),
            "characters": parse_tags_dict_list(
                [character.to_dict() for character in characters]
            ),
            "groups": parse_tags_dict_list([group.to_dict() for group in groups]),
            "language": parse_tags_dict_list(
                [language_info.to_dict() for language_info in language_infos]
            ),
            "series": parse_tags_dict_list([parody.to_dict() for parody in parodies]),
            "tag": tag_list,
            "female": female_list,
            "male": male_list,
            "type": parse_tags_dict_list([type.to_dict() for type in types]),
        }
