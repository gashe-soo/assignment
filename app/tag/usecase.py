from app.tag.dtos import CreateTagDto
from app.tag.models import Tag
from app.tag.repository import TagRepository


class TagUsecase:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository

    async def create_tags(self, tags: list[CreateTagDto]) -> list[Tag]:
        return await self.repository.create_tags(tags)

    async def get_tag_by_name(self, name: str, locale: str) -> Tag:
        # TODO : Implement this method
        raise NotImplementedError
