from app.tag.dtos import CreateTagDto
from app.tag.models import Tag


class TagUsecase:
    async def create_tags(self, tags: list[CreateTagDto]) -> list[Tag]:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_tag_by_name(self, name: str, locale: str) -> Tag:
        # TODO : Implement this method
        raise NotImplementedError
