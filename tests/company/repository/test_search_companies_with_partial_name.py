import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTranslation
from app.company.repository import CompanyRepository
from app.core.enums import Locale


@pytest.mark.asyncio
async def test_it_should_return_matches_if_partial_name_exists(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    company_1 = Company()
    company_1.translations = [
        CompanyTranslation(name="지오 코리아", locale=Locale.KO),
        CompanyTranslation(name="GEOCM Co.", locale=Locale.EN),
        CompanyTranslation(name="GEOCM", locale=Locale.JP),
    ]

    company_2 = Company()
    company_2.translations = [
        CompanyTranslation(name="지오지", locale=Locale.KO),
    ]
    session.add_all([company_1, company_2])
    await session.flush()

    # When
    results = await repository.search_companies_with_partial_name("지오")

    # Then
    assert len(results) == 2
    assert {result.name for result in results} == {
        "지오 코리아",
        "지오지",
    }


@pytest.mark.asyncio
async def test_it_should_return_empty_list_if_partial_name_not_found(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    company = Company()
    company.translations = [
        CompanyTranslation(name="라인 프레쉬", locale=Locale.KO),
        CompanyTranslation(name="LINE FRESH", locale=Locale.EN),
    ]
    session.add(company)
    await session.flush()

    # When
    results = await repository.search_companies_with_partial_name("아무회사")

    # Then
    assert results == []
