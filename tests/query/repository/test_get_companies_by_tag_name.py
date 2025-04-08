import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTag, CompanyTranslation
from app.query.repository import QueryRepository
from app.tag.models import Tag, TagTranslation


@pytest.mark.asyncio
async def test_get_companies_by_tag_names_should_return_company_infos(
    session: AsyncSession, repository: QueryRepository
) -> None:
    # Given
    tag = Tag(
        translations=[
            TagTranslation(name="기술", locale="ko"),
            TagTranslation(name="Tech", locale="en"),
        ]
    )
    session.add(tag)
    await session.flush()

    company = Company()
    company.translations = [
        CompanyTranslation(name="라인", locale="ko"),
        CompanyTranslation(name="LINE", locale="en"),
    ]
    company.tags = [CompanyTag(tag_id=tag.id, tag=tag)]
    session.add(company)
    await session.flush()

    # When
    result = await repository.get_companies_by_tag_name("기술")

    # Then
    assert len(result) == 2

    ko_info = next(r for r in result if r.locale == "ko")
    assert ko_info.company_info.name == "라인"
    assert "기술" in ko_info.company_info.tags

    en_info = next(r for r in result if r.locale == "en")
    assert en_info.company_info.name == "LINE"
    assert "Tech" in en_info.company_info.tags


@pytest.mark.asyncio
async def test_get_companies_by_tag_names_should_return_empty_if_not_found(
    session: AsyncSession, repository: QueryRepository
) -> None:
    # When
    result = await repository.get_companies_by_tag_name("없는태그")

    # Then
    assert result == []
