import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.tag.models import Tag, TagTranslation
from app.tag.repository import TagRepository


@pytest.mark.asyncio
async def test_it_should_return_existing_tag(
    session: AsyncSession, repository: TagRepository
) -> None:
    # Given
    tag = Tag(
        translations=[
            TagTranslation(name="신규태그", locale="ko"),
            TagTranslation(name="New_tag", locale="en"),
        ]
    )
    session.add(tag)
    await session.flush()

    # When
    result = await repository.get_tag_by_name("신규태그")

    # Then
    assert result is not None
    assert isinstance(result, Tag)
    assert result.id == tag.id


@pytest.mark.asyncio
async def test_it_should_return_none_when_not_found(
    repository: TagRepository,
) -> None:
    # When
    result = await repository.get_tag_by_name("없는태그")

    # Then
    assert result is None


@pytest.mark.asyncio
async def test_it_should_return_first_when_duplicates_exist(
    session: AsyncSession, repository: TagRepository
) -> None:
    # Given
    tag1 = Tag(translations=[TagTranslation(name="common", locale="ko")])
    tag2 = Tag(translations=[TagTranslation(name="common", locale="en")])
    session.add_all([tag1, tag2])
    await session.flush()

    # When
    result = await repository.get_tag_by_name("common")

    # Then
    assert result is not None
    assert result.id in {tag1.id, tag2.id}
