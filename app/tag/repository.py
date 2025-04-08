from app.tag.dtos import CreateTagDto
from app.tag.models import Tag


class TagRepository:
    async def create_tags(
        self, tags: list[CreateTagDto]
    ) -> list[CreateTagDto]:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_tag_by_name(self, name: str) -> Tag | None:
        # TODO: Implement this method
        raise NotImplementedError
