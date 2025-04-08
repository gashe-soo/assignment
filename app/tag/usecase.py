from app.tag.dtos import CreateTagDto, TagNameWithLocale


class TagUsecase:
    async def create_tags(
        self, tags: list[CreateTagDto]
    ) -> list[CreateTagDto]:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_tag_by_name(
        self, name: str, locale: str
    ) -> list[TagNameWithLocale]:
        # TODO : Implement this method
        raise NotImplementedError
