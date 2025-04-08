import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTag, CompanyTranslation
from app.query.repository import QueryRepository
from app.tag.models import Tag, TagTranslation


@pytest.mark.asyncio
async def test_get_companies_info_should_return_company_data_by_locale(
    session: AsyncSession, repository: QueryRepository
) -> None:
    # Given
    company = Company(id=1)
    company.translations = [
        CompanyTranslation(name="라인", locale="ko"),
        CompanyTranslation(name="LINE", locale="en"),
    ]

    tag1 = Tag(
        id=10,
        translations=[
            TagTranslation(name="기술", locale="ko"),
            TagTranslation(name="Tech", locale="en"),
        ],
    )
    tag2 = Tag(
        id=11,
        translations=[
            TagTranslation(name="디자인", locale="ko"),
            TagTranslation(name="Design", locale="en"),
        ],
    )
    company.tags = [
        CompanyTag(tag=tag1),
        CompanyTag(tag=tag2),
    ]

    session.add(company)
    await session.flush()

    # When
    result = await repository.get_companies_info([1])

    # Then
    assert len(result) == 2

    ko_result = next(r for r in result if r.locale == "ko")
    assert ko_result.company_info.name == "라인"
    assert set(ko_result.company_info.tags) == {"기술", "디자인"}

    en_result = next(r for r in result if r.locale == "en")
    assert en_result.company_info.name == "LINE"
    assert set(en_result.company_info.tags) == {"Tech", "Design"}
