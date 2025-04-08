from sqlalchemy import select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from app.tag.dtos import CreateTagDto
from app.tag.models import Tag, TagTranslation


class TagRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tags(self, tags: list[CreateTagDto]) -> list[Tag]:
        created_tags: list[Tag] = []
        seen_tag_ids: set[int] = set()

        for dto in [dto for dto in tags if dto.tag_name]:
            name_locale_pairs = [
                (item.name, item.locale) for item in dto.tag_name
            ]
            stmt = (
                select(Tag)
                .join(TagTranslation)
                .where(
                    tuple_(TagTranslation.name, TagTranslation.locale).in_(
                        name_locale_pairs
                    )
                )
                .limit(1)
            )
            result = await self.session.execute(stmt)
            found_tag = result.scalar_one_or_none()

            if found_tag and found_tag.id not in seen_tag_ids:
                created_tags.append(found_tag)
                seen_tag_ids.add(found_tag.id)
            else:
                new_tag = Tag()
                new_tag.translations = [
                    TagTranslation(name=item.name, locale=item.locale)
                    for item in dto.tag_name
                ]
                self.session.add(new_tag)
                await self.session.flush()

                created_tags.append(new_tag)
                seen_tag_ids.add(new_tag.id)

        return created_tags

    async def get_tag_by_name(self, name: str) -> Tag | None:
        stmt = (
            select(Tag)
            .join(TagTranslation)
            .where(TagTranslation.name == name)
            .limit(1)
        )

        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result if result else None
