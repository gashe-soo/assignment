import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tag.dtos import CreateTagDto, TagNameWithLocale
from app.tag.models import Tag, TagTranslation
from app.tag.repository import TagRepository


@pytest.mark.asyncio
async def test_it_should_create_or_reuse(
    session: AsyncSession, repository: TagRepository
) -> None:
    # Given
    tag = Tag(
        translations=[
            TagTranslation(locale="en", name="Design"),
            TagTranslation(locale="ko", name="디자인"),
        ]
    )
    session.add(tag)
    await session.flush()

    # And
    dto1 = CreateTagDto(
        tag_name=[
            TagNameWithLocale(locale="en", name="Design"),
            TagNameWithLocale(locale="ko", name="디자인"),
        ]
    )
    dto2 = CreateTagDto(
        tag_name=[
            TagNameWithLocale(locale="en", name="Development"),
            TagNameWithLocale(locale="ko", name="개발"),
        ]
    )

    # When:
    result = await repository.create_tags([dto1, dto2])

    # Then:
    assert len(result) == 2
    stmt = select(TagTranslation).where(
        TagTranslation.tag_id.in_([tag.id for tag in result])
    )
    result = (await session.execute(stmt)).scalars().all()
    names = [translation.name for translation in result]
    assert "디자인" in names
    assert "개발" in names
