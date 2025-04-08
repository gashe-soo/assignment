import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTag, CompanyTranslation
from app.company.repository import CompanyRepository
from app.core.enums import Locale
from app.tag.models import Tag


@pytest.mark.asyncio
async def test_it_should_return_companies_by_tag_id(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    tag = Tag()
    session.add(tag)
    await session.flush()

    company1 = Company()
    company1.translations = [
        CompanyTranslation(name="라인 프레쉬", locale=Locale.KO)
    ]
    company1.tags = [CompanyTag(tag_id=tag.id)]

    company2 = Company()
    company2.translations = [CompanyTranslation(name="원티드랩", locale=Locale.KO)]
    company2.tags = [CompanyTag(tag_id=tag.id)]

    session.add_all([company1, company2])
    await session.flush()

    # When
    companies = await repository.get_companies_by_tag_id(tag_id=tag.id)

    # Then
    assert len(companies) == 2
    names = [t.name for c in companies for t in c.translations]
    assert "라인 프레쉬" in names
    assert "원티드랩" in names


@pytest.mark.asyncio
async def test_it_should_return_empty_list_when_no_company_has_tag(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    tag = Tag()
    session.add(tag)
    await session.flush()

    # When
    companies = await repository.get_companies_by_tag_id(tag_id=tag.id)

    # Then
    assert companies == []
